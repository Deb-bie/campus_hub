import express from 'express';
import cors from 'cors'
import helmet from 'helmet'
import compression from 'compression'
import dotenv from 'dotenv'
import logger from './utils/logger'
import routes from './routes/index'
import errorHandler from './middleware/errorHandler'
import { loadEnv } from './config/config';
import { startConsumer } from './config/kafka_consumer';


dotenv.config();
const PORT = process.env.PORT;
loadEnv()

const app = express();

app.use(helmet());
app.use(cors({origin: '*'}));
app.use(compression());
app.use(express.json());
app.use(express.urlencoded({ extended: true }));


const apiPrefix = process.env.API_PREFIX;
app.use(apiPrefix!, routes);

app.get('/health', (req, res) => {
  res.json(
    { 
      status: 'OK', 
      service: 'search-service', 
      timestamp: new Date().toISOString() 
    }
  );
});

app.use(errorHandler);


app.use('*', (req, res) => {
  res.status(404).json({ 
    error: 'Route not found' 
  });
});


app.listen(PORT, () => {
  logger.info(`Search service running on port ${PORT}`);
  logger.info(`Environment: ${process.env.ENV}`);
  startConsumer();
});
