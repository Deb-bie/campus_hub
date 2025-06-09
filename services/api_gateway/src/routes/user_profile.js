const { createProxyMiddleware } = require('http-proxy-middleware');
const express = require('express');

const { authenticateJWT} = require('../middlewares/auth_middleware');

const router = express.Router();

// Middleware to parse JSON bodies (important for proxy)
router.use(express.json());
router.use(express.urlencoded({ extended: true }));


// Test endpoint to verify auth is working
router.get('/test-auth', authenticateJWT, (req, res) => {
  res.json({
    message: 'Auth working',
    user: req.user,
    timestamp: new Date().toISOString()
  });
});



// User Profile Service Proxy
router.use(
  '/',
  authenticateJWT,
  createProxyMiddleware({
    target: process.env.USER_PROFILE_SERVICE_URL,
    changeOrigin: true,

    selfHandleResponse: false,

    on: {

      proxyReq: (proxyReq, req, res) => {
        let userEmail = null;
        
        if (req.user) {
          userEmail = req.user.sub;
          proxyReq.setHeader('x-user-email', userEmail);
        } else {
          console.error('CRITICAL: No user email found in token');
          console.error('Available user fields:', Object.keys(req.user || {}));
          console.error('Full req.user object:', req.user);
          console.error('Proceeding with proxy but service will likely reject...');
          console.error('Cannot set user headers - no email found');
          res.status(401).json({ error: 'Invalid token: missing user email' });
        }
    
        if (req.headers.authorization) {
          proxyReq.setHeader('authorization', req.headers.authorization);
        }
      },

      error: (err, req, res) => {
        console.error('Proxy error:', {
          message: err.message,
          code: err.code,
          method: req.method,
          url: req.url,
          target: process.env.USER_PROFILE_SERVICE_URL
        });

        if (!res.headersSent) {
          res.status(502).json({
            error: 'Service unavailable',
            message: 'User profile service is currently unavailable',
            details: process.env.NODE_ENV === 'development' ? err.message : undefined,
            timestamp: new Date().toISOString()
          });
        }
      }
    },

    pathRewrite: {
      '^/user-profile': '', // Remove /user-profile prefix
    }
  }),
);

module.exports = router;
