const axios = require('axios');

const AUTH_SERVICE_URL = process.env.AUTH_SERVICE_URL;

if (!AUTH_SERVICE_URL) {
  console.error('AUTH_SERVICE_URL environment variable is not set');
  process.exit(1);
}

/**
 * Helper function to handle auth service requests
 */
const proxyToAuthService = async (req, res, endpoint, includeAuth = false) => {
  try {
    const config = {
      method: req.method,
      url: `${AUTH_SERVICE_URL}${endpoint}`,
      data: req.body,
      headers: {
        'Content-Type': 'application/json'
      }
    };

    // Include authorization header if required
    if (includeAuth && req.headers.authorization) {
      config.headers.authorization = req.headers.authorization;
    }

    console.log(`📡 Proxying to auth service: ${config.method} ${config.url}`);
    
    const response = await axios(config);
    
    console.log(`Auth service response: ${response.status}`);
    res.status(response.status).json(response.data);
    
  } catch (error) {
    console.error('Auth service error:', {
      message: error.message,
      status: error.response?.status,
      data: error.response?.data,
      url: `${AUTH_SERVICE_URL}${endpoint}`
    });
    
    if (error.response) {
      res.status(error.response.status).json(error.response.data);
    } else if (error.code === 'ECONNREFUSED') {
      res.status(503).json({
        error: 'Service unavailable',
        message: 'Authentication service is currently unavailable'
      });
    } else {
      res.status(500).json({
        error: 'Internal server error',
        message: 'Unable to process authentication request'
      });
    }
  }
};

/**
 * Login user
 * POST /auth/login
 */
const signin = async (req, res) => {
  await proxyToAuthService(req, res, '/signin');
};

/**
 * Register new user
 * POST /auth/register
 */
const signup = async (req, res) => {
  await proxyToAuthService(req, res, '/signup');
};


module.exports = {
  signin,
  signup
};

