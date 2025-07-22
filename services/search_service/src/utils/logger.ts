import winston from 'winston'
import path from 'path'
import { loadEnv } from '../config/config';

loadEnv()

const logLevel = process.env.LOG_LEVEL!;
const logFile = process.env.LOG_FILE!;

const logger = winston.createLogger({
  level: logLevel,
  format: winston.format.combine(
    winston.format.timestamp(),
    winston.format.errors({ stack: true }),
    winston.format.json()
  ),
  defaultMeta: { service: 'search-service' },
  transports: [
    new winston.transports.File({ 
      filename: path.resolve(logFile),
      maxsize: 5242880,
      maxFiles: 5
    })
  ]
});

if (process.env.ENV !== 'production') {
  logger.add(new winston.transports.Console({
    format: winston.format.combine(
      winston.format.colorize(),
      winston.format.simple()
    )
  }));
}

export default logger;
