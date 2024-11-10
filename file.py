"""csv related module"""
import csv

def save_to_file(file_name, jobs):
    """convert gathered job information to file """
    with open(f"{file_name}.csv", "w", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["Position", "Company", "Link", "Location"])
        value_list = [job.values() for job in jobs]
        writer.writerows(value_list)