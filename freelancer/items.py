from scrapy.item import Item, Field
from itemloaders.processors import MapCompose, TakeFirst
import re

def extract_votes_number(text):
    try:
        return text.split()[0]
    except:
        return 'no available'

class FreelancerItem(Item):
    username  = Field(
        input_processor = MapCompose(str.strip),
        output_processor = TakeFirst()
    )
    oneliner  = Field(
        input_processor = MapCompose(str.strip),
        output_processor = TakeFirst()
    )
    rating  = Field(
        input_processor = MapCompose(str.strip),
        output_processor = TakeFirst()
    )
    location  = Field(
        input_processor = MapCompose(str.strip),
        output_processor = TakeFirst()
    )
    member_since  = Field(
        input_processor = MapCompose(str.strip),
        output_processor = TakeFirst()
    )
    jobs_completed_rate  = Field(
        input_processor = MapCompose(str.strip),
        output_processor = TakeFirst()
    )
    on_budget_completed_rate  = Field(
        input_processor = MapCompose(str.strip),
        output_processor = TakeFirst()
    )
    on_time_rate  = Field(
        input_processor = MapCompose(str.strip),
        output_processor = TakeFirst()
    )
    repeat_hire_rate  = Field(
        input_processor = MapCompose(str.strip),
        output_processor = TakeFirst()
    )
    user_skills  = Field(
        input_processor = MapCompose(str.strip),
        output_processor = TakeFirst()
    )
    user_certifications  = Field(
        input_processor = MapCompose(str.strip),
        output_processor = TakeFirst()
    )
    avg_price  = Field(
        input_processor = MapCompose(str.strip),
        output_processor = TakeFirst()
    )