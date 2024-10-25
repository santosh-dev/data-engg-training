from pyflink.table import EnvironmentSettings,TableEnvironment
from faker import Faker

# create a batch table env
env = EnvironmentSettings.in_batch_mode()
table_env = TableEnvironment.create(env)

# env = TableEnvironment.get_execution_environment()
# env.set_runtime_mode(EnvironmentSettings.in_batch_mode())
# # write all the data to one file
# env.set_parallelism(1)

# initilize faker
fake = Faker()
data = [(fake.name(),fake.city(),fake.state()) for _ in range(10)]

# generate fake data and convert to pyflink table
# for x in range(10):
#     data.append(fake.name(),fake.city(),fake.state())

# define column names
column_names = ["name","city","state"]

# create pyflink table
table = table_env.from_elements(data,schema=column_names)

# print the table
table.execute().print()