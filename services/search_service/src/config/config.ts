import dotenv from 'dotenv'
import path from 'path'

export function loadEnv() {
    const env = process.env.ENV || 'development';

    const envfileMap: any = {
        development: '.env',
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

export const config = {
    cors: {
        origin: process.env.CORS_ORIGIN || '*',
        methods: ['GET', 'PUT', 'PATCH', 'OPTIONS', 'POST', 'DELETE'],
        allowedHeaders: ['Content-Type', 'Authorization', 'X-Requested-With'],
        preflightContinue: false,
        optionsSuccessStatus: 204
    }
}
