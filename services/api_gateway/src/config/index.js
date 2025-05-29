const dotenv = require('dotenv');
const path = require('path');

function loadEnv() {
    const env = process.env.NODE_ENV || 'development';

    const envfileMap = {
        development: '.env.dev',
        production: '.env.prod',
        docker: '.env.docker'
    };

    const envFile = envfileMap[env] || '.env';
    const envPath = path.resolve(process.cwd(), envFile);
    const result = dotenv.config({ path: envPath });
    
    if (result.error) {
        console.warn(`⚠️  Could not load environment file: ${envPath}`);
        console.warn(`Using default environment variables.`);
        throw result.error;
    }
    
    console.log(`Environment variables loaded from ${envFile}`);
}

const config = {
    cors: {
        origin: process.env.CORS_ORIGIN || '*',
        methods: ['GET', 'PUT', 'PATCH', 'OPTIONS', 'POST', 'DELETE'],
        allowedHeaders: ['Content-Type', 'Authorization', 'X-Requested-With'],
        preflightContinue: false,
        optionsSuccessStatus: 204
    }
}

module.exports = { loadEnv, config };