/**
 * API Gateway Server Entry Point
*
*/

require('dotenv').config();
const app = require('./src/app');

const PORT = process.env.PORT;

// Start server
app.listen(PORT, () => {
    console.log(`API Gateway is running at http://localhost:${PORT}`);
});

// Graceful shutdown
const gracefulShutdown = (signal) => {
    console.log(`${signal} received, shutting down gracefully`);
  
    server.close(() => {
        console.log(`HTTP server closed`);
        
        process.exit(0);
    });

    // Force close after 10 seconds
    setTimeout(() => {
        console.log(`Forced shutdown after timeout`);

        process.exit(1);
    }, 10000);
};

process.on('SIGTERM', () => gracefulShutdown('SIGTERM'));
process.on('SIGINT', () => gracefulShutdown('SIGINT'));

// Handle uncaught exceptions
process.on('uncaughtException', (error) => {
  console.log(`Uncaught Exception: ${error}`);
  process.exit(1);
});

process.on('unhandledRejection', (reason, promise) => {
  console.log(`Unhandled Rejection at:, ${promise}, reason:, ${reason}`);
  process.exit(1);
});



