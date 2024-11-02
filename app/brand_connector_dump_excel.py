import json
import pandas

with (open('brands.json', 'r') as brands_file,
      open('output.json', 'r', encoding='utf-8') as output_file):
    brands: list[dict[str, str]] = json.load(brands_file)
    outputs: list[dict[str, str]] = json.load(output_file)
    for output in outputs:
        output['brand'] = ''
        for brand in brands:
            if brand['brand'] in output['title'].lower():
                output['brand'] = brand['brand']
                break
pd = pandas.DataFrame(outputs)
pd.to_excel('parse.xlsx', index=False)
# with open('output_with_brand.json', 'w', encoding='utf-8') as f:
#     json.dump(outputs, f, ensure_ascii=False, indent=4)

