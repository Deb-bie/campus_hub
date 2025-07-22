import { Kafka } from 'kafkajs';
import { loadEnv } from './config';
import eventController from '../controllers/eventController';


loadEnv()

const kafka = new Kafka(
    { 
        clientId: process.env.CLIENT_ID, 
        brokers: [process.env.KAFKA_BROKER!]
    }
);

const consumer = kafka.consumer(
    {
        groupId: process.env.GROUP_ID!
    }
);


export const startConsumer = async () => {
    await consumer.connect();

    await consumer.subscribe(
        { 
            topic: 'event_created', 
            fromBeginning: true 
        }
    );

    await consumer.subscribe(
        { 
            topic: 'event_updated', 
            fromBeginning: true 
        }
    );
    
    await consumer.subscribe(
        { 
            topic: 'event_deleted', 
            fromBeginning: true 
        }
    );

    await consumer.run({
        eachMessage: async ({ topic, message }) => {
            const value = message.value?.toString();
            const payload = JSON.parse(value!);

            if (topic === 'event_created') {
                await eventController.indexEventToElastic(payload.metadata)
            } else if (topic === 'event_updated') {
                await eventController.updateEventInElastic(payload.metadata)
            }
        }
    });
};