from scrapy.item import Item, Field
from itemloaders.processors import MapCompose, TakeFirst
from datetime import datetime

datetime_object = datetime.strptime('Jun 1 2005  1:33PM', '%b %d %Y %I:%M%p')

def clean_username(text):
    return text[1::]

def parse_date(text):
    return text
    return datetime.strptime(text.replace('Joined ', ''), '%b %d, %Y')

class FreelancerItem(Item):
    username  = Field(
        input_processor = MapCompose(clean_username),
        output_processor = TakeFirst()
    )
    description  = Field(
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
    price_per_hour  = Field(
        input_processor = MapCompose(str.strip),
        output_processor = TakeFirst()
    )