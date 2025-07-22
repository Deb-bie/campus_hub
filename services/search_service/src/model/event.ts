export interface Event {
    id: string;
    name: string;
    description: string;
    short_description: string;
    organizer_id: string;
    location: string;
    start_time: string;
    end_time: string;
    category: string;
    image_url: string;
    capacity: string
    tags: string;
    is_public: boolean;
    is_virtual: boolean;
    is_recurring: boolean;
    is_free: boolean;
    fee: number;
    virtual_meeting_link: string;
    status: string;
}