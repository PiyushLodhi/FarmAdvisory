import io
import json
from snips_nlu import SnipsNLUEngine
from snips_nlu.default_configs import CONFIG_EN

engine = SnipsNLUEngine(config = CONFIG_EN)

with io.open("dataset1.json") as f:
	dataset = json.load(f)

engine.fit(dataset)

parsing = engine.parse("Maize is a Uttar Pradesh crop")

# json_output = json.dumps(parsing, indent=2)
print(parsing)
# slots = parsing

# for slot in slots:
# 	print(slot)
# 	print('*******************')
