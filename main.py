from script import initiaite_process

if __name__ =="__main__":

    job_positions =[
              "Cloud Engineer", "GCP Engineer", "Azure Engineer", "AWS Engineer", "Big Data Engineer",
              "Site Reliability Engineer","DevOps Engineer","Python Engineer","Data Engineer"]
              
    for position in job_positions:
        initiaite_process(position)
        print(position)