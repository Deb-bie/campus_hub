
/**
 * 404 Not Found handler
 */
const notFoundHandler = (req, res, next) => {
  res.status(404).json({
    error: 'Route not found',
    message: `The requested route ${req.method} ${req.originalUrl} was not found`,
    timestamp: new Date().toISOString()
  });
};

/**
 * Global error handler
 */
const globalErrorHandler = (error, req, res, next) => {
  console.error('🔥 Unhandled error:', {
    message: error.message,
    stack: error.stack,
    url: req.originalUrl,
    method: req.method,
    ip: req.ip || req.connection.remoteAddress
  });
  
  // Don't expose error details in production
  const isDevelopment = process.env.NODE_ENV === 'development';
  
  res.status(error.status || 500).json({
    error: 'Internal server error',
    message: isDevelopment ? error.message : 'An unexpected error occurred',
    timestamp: new Date().toISOString(),
    ...(isDevelopment && { stack: error.stack })
  });
};

module.exports = {
  notFoundHandler,
  globalErrorHandler
};


