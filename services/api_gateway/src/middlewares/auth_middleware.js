const jwt = require('jsonwebtoken');

const JWT_SECRET = process.env.JWT_SECRET;

if (!JWT_SECRET) {
  console.error('JWT_SECRET environment variable is not set');
  process.exit(1);
}

const authenticateJWT = (req, res, next) => {
  const authHeader = req.headers.authorization;
  
  if (!authHeader || !authHeader.startsWith('Bearer ')) {
    return res.status(401).json({
      error: 'Access denied',
      message: 'No token provided or invalid format. Expected: Bearer <token>'
    });
  }

  const token = authHeader.substring(7);

  try {
    const decoded = jwt.verify(token, Buffer.from(process.env.JWT_SECRET, 'base64'));
    
    req.user = decoded;
    next();
  } catch (error) {
    console.error('JWT verification failed:', {
      error: error.message,
      name: error.name,
      token: token.substring(0, 20) + '...' // Logging first 20 chars
    });
    
    let message = 'Token verification failed';
    if (error.name === 'TokenExpiredError') {
      message = 'Token has expired';
    } else if (error.name === 'JsonWebTokenError') {
      message = 'Invalid token format';
    }

    return res.status(403).json({
      error: 'Invalid token',
      message: message
    });
  }
};


module.exports = {
  authenticateJWT
};

