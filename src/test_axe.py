from utils.watch import configure_logger
from scan_axe import axe_the_things

# Set up logger
output = []
configure_logger(output)

# Test the axe_the_things function
target = "https://civicactions.com"
url_id = 1
axe_the_things(target, url_id)

# Print the output
print(output)
