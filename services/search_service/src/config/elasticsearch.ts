import { Client } from '@elastic/elasticsearch';
import logger from '../utils/logger';
import { loadEnv } from './config';

loadEnv()

const client = new Client({
  node: process.env.ELASTICSEARCH_NODE!,
});

client.info().then(console.log).catch(console.error);

export const testConnection = async () => {
  try {
    const health = await client.cluster.health();
    logger.info('Elasticsearch connection established', { status: health.status });
    return true;
  } catch (error) {
    logger.error('Elasticsearch connection failed', error);
    return false;
  }
};

export default client;
