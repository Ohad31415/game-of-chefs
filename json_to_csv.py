import csv

def json_to_csv(data_dict):
    with open("./recipies.csv", "w") as write_CSV1:
        columns = list(data_dict[0].keys())
        writer = csv.DictWriter(write_CSV1, fieldnames=columns)
        writer.writeheader()
        for record in range(len(data_dict)):
            temp = {}
            for field in columns:
                temp[field] = data_dict[record][field]
            writer.writerow(temp)