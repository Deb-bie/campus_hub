import client from "../config/elasticsearch";
import logger from "../utils/logger";
import { Event } from "../model/event";



class EventsController {

    async indexEventToElastic(event: Event) {
        try {
           await client.index(
            {
                index: process.env.ELASTICSEARCH_INDEX!,
                id: event.id,
                document: event
            }
           );
           logger.info(`Event indexed with ID: ${event.id}`);

        } catch (error) {
            logger.error('Error indexing event to Elasticsearch', error);
            throw error;
        }   
    }

    async updateEventInElastic(event: Event) {
        try {
            await client.update(
                {
                    index: process.env.ELASTICSEARCH_INDEX!,
                    id: event.id,
                    doc: event
                }
            );
            logger.info(`Event updated with ID: ${event.id}`);
        } catch (error) {
            logger.error('Error updating event in Elasticsearch', error);
            throw error;
        }
    }

    async deleteEventInElastic (eventId: string) {
        try {
            await client.delete(
                {
                    index: process.env.ELASTICSEARCH_INDEX!,
                    id: eventId,
                }
            );

            logger.info(`Event deleted from Elasticsearch with ID: ${eventId}`);
        } catch (error) {
            logger.error('Error deleting event from Elasticsearch', error);
            throw error;
        }
    }

}

export default new EventsController()
