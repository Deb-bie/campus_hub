const { createProxyMiddleware } = require('http-proxy-middleware');
const express = require('express');
const { authenticateJWT} = require('../middlewares/auth_middleware');
const router = express.Router();

router.use(express.json());
router.use(express.urlencoded({ extended: true }));

const target = process.env.EVENTS_SERVICE_URL;

router.use(
  '/explore-events',
  createProxyMiddleware({
    target: target,
    changeOrigin: true,
    pathRewrite: { 
      '^/': 'api/events/explore-events/' 
    }
  
  }),
);

router.use(
  '/this-week',
  createProxyMiddleware({
    target: target,
    changeOrigin: true,
    pathRewrite: { 
      '^/': 'api/events/this-week/' 
    }
  
  }),
);

router.use(
  '/upcoming',
  createProxyMiddleware({
    target: target,
    changeOrigin: true,
    pathRewrite: { 
      '^/': 'api/events/upcoming/' 
    }
  
  }),
);

router.use(
  '/feed',
  createProxyMiddleware({
    target: target,
    changeOrigin: true,
    pathRewrite: { 
      '^/': 'api/events/feed/' 
    }
  
  }),
);



router.use(
  '/',
  authenticateJWT,
  createProxyMiddleware({
    target: target,
    changeOrigin: true,

    on: {
      proxyReq: (proxyReq, req, res) => {
        let userEmail = null;
        
        if (req.user) {
          userEmail = req.user.sub;
          
        } else{
          console.error('CRITICAL: No user email found in token');
          console.error('Available user fields:', Object.keys(req.user || {}));
          console.error('Full req.user object:', req.user);
          console.error('Proceeding with proxy but service will likely reject...');
        }
      

        if (['POST', 'PUT', 'PATCH'].includes(req.method.toUpperCase())) {
          const bodyData = JSON.stringify(req.body);

          if (bodyData && userEmail) {

            console.log("Proxying to events service: Headers set ", {
              target: target
            })

            proxyReq.setHeader('Content-Type', 'application/json');
            proxyReq.setHeader('Content-Length', Buffer.byteLength(bodyData));
            proxyReq.setHeader('x-user-email', userEmail);
            proxyReq.setHeader('authorization', req.headers.authorization)
            proxyReq.write(bodyData);
          }
          else{
            console.error('Cannot set user headers - no email found');
            res.status(401).json({ error: 'Invalid token: missing user email' });
          }
        }
        
        else {
          if (userEmail) {
            console.log("Proxying to events service: Headers set ", {
              target: target
            })
            proxyReq.setHeader('x-user-email', userEmail);
            proxyReq.setHeader('authorization', req.headers.authorization)
          } 
        }
        
      },

      error: (err, req, res) => {
        console.error('Proxy error:', {
          message: err.message,
          code: err.code,
          method: req.method,
          url: req.url,
          target: target
        });

        if (!res.headersSent) {
          res.status(502).json({
            error: 'Service unavailable',
            message: 'Events service is currently unavailable',
            details: process.env.NODE_ENV === 'development' ? err.message : undefined,
            timestamp: new Date().toISOString()
          });
        }
      }
    },

    pathRewrite: {
      '^': '/api/events/',
    }

  })
);




module.exports = router;

