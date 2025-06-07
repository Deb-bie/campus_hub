const express = require('express');
const cors = require('cors');
const helmet = require('helmet');

const { globalErrorHandler, notFoundHandler } = require('./middlewares/error_handlers');
const {loadEnv, config} = require("./config/index");
const authRoutes = require('./routes/auth');
const userProfileRoutes = require('./routes/user_profile');
const eventsRoutes = require("./routes/events");

require('dotenv').config();

loadEnv();

const app = express();

// Security middleware
app.use(helmet());
app.use(cors(config.cors));

app.use(express.json());


// Routes
app.use('/api/auth', authRoutes)
app.use('/api/user-profile', userProfileRoutes);
app.use('/api/events', eventsRoutes)


// Health check (before error handler)
app.get('/health', (req, res) => {
  res.json({
    status: 'healthy',
    service: 'API Gateway',
    timestamp: new Date().toISOString(),
    version: process.env.npm_package_version || '1.0.0',
    uptime: process.uptime()
  });
});


// Error handling middleware (must be last)
app.use(notFoundHandler);
app.use(globalErrorHandler);


module.exports = app;
