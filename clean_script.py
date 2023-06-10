import json
 
 
INPUT = "parsed_articles.jl"
OUTPUT = "clean_data.jl"
 
f_input = open(INPUT, "r", encoding="utf-8")
f_output = open(OUTPUT, "w", encoding="utf-8")
for line in f_input:
    data = json.loads(line)
    was_faulty = False
    for key in data:
        if "gpt3" in key and "gpt3_crimes" not in key:
            try:
                string_record = data[key].rstrip(".")
                dict_record = json.loads(string_record)
                data[key] = dict_record
            except Exception as e:
                print(e)
                was_faulty = True
                break
    
    if (was_faulty):
        continue
    data.pop("clean", None)
    new_data = json.dumps(data, ensure_ascii=False)
    f_output.write(new_data + "\n")