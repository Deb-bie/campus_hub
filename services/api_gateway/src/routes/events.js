const { createProxyMiddleware } = require('http-proxy-middleware');
const express = require('express');
const { authenticateJWT} = require('../middlewares/auth_middleware');
const router = express.Router();

router.use(express.json());
router.use(express.urlencoded({ extended: true }));

const target = process.env.EVENTS_SERVICE_URL;

// No jwt urls
router.use(
  ['/events/public-feed'],
  createProxyMiddleware({
    target,
    changeOrigin: true,
    pathRewrite: { '^/events': '' },
  })
);

// Jwt required
router.use(
  ['/events/create'],
  authenticateJWT,
  createProxyMiddleware({
    target,
    changeOrigin: true,
    selfHandleResponse: false,

    on: {
      proxyReq: (proxyReq, req, res) => {
        let userEmail = null;
        
        if (req.user) {
          userEmail = req.user.sub;
        }
      
        if (!userEmail) {
          console.error('CRITICAL: No user email found in token');
          console.error('Available user fields:', Object.keys(req.user || {}));
          console.error('Full req.user object:', req.user);
          console.error('Proceeding with proxy but service will likely reject...');
        }
        
        if (userEmail) {
          proxyReq.setHeader('x-user-email', userEmail);
        } else{
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
      '^/events': '',
    }

  })
);

module.exports = router;

