import random
import sys
from faker import Faker
from app import db
from app.models import Students

def create_fake_users(n):
    """Generate fake users."""
    faker = Faker()
    specialization_list=['CSE','ECE','EEE','ISE']
    section_list=['A','B','C','D']
    for i in range(n):
        user = Students(
                    usn="1AM"+str(random.randint(18,22))+"CS"+str(random.randint(000,100)),
                    name=faker.name(),
                    age=random.randint(20, 80),
                    address=faker.address().replace('\n', ', '),
                    phone=faker.phone_number(),
                    email=faker.email(),
                    yoa =random.randint(2018,2022), 
                    specialization = random.choice(specialization_list),
                    semester = random.randint(1,4),
                    section=random.choice(section_list),
        )
        db.session.add(user)
    db.session.commit()
    print(f'Added {n} fake users to the database.')


if __name__ == '__main__':
    if len(sys.argv) <= 1:
        print('Pass the number of users you want to create as an argument.')
        sys.exit(1)
    create_fake_users(int(sys.argv[1]))
