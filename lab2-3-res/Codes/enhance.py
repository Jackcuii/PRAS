import os

os.environ["http_proxy"]  = 'http://127.0.0.1:7890'
os.environ["https_proxy"]  = 'http://127.0.0.1:7890'


from sentence_transformers import SentenceTransformer
from umap import UMAP
from sklearn.cluster import KMeans
import pandas as pd
import json


with open("./AP_Deckard.txt", "r", encoding="utf-8") as file:
    content1 = file.read()

inputs1 = content1.split('\n')

embedding_model = SentenceTransformer('thenlper/gte-small',cache_folder="models")
embeddings = embedding_model.encode(inputs1, show_progress_bar=True)

embeddings.shape


def try_reduce_dim(dim):
    # Create an embedding for each abstract
    print("-------------------- Reduce Dimension to", dim, "--------------------")
    
    umap_model = UMAP(
        n_components=dim, min_dist=0.0, metric='cosine', random_state=42
    )
    reduced_embeddings = umap_model.fit_transform(embeddings)

    # 使用 KMeans 将数据聚类为两类
    kmeans = KMeans(n_clusters=2, random_state=42)
    clusters = kmeans.fit_predict(reduced_embeddings)

    # 查看聚类结果
    print(len(clusters))
    print(clusters)
    # clusters

    # with open("AP.txt", "r", encoding="utf-8") as file:
    # with open("Bili.txt", "r", encoding="utf-8") as file:

    #with open("AP_llm.json", "r", encoding="utf-8") as file:
    #with open("Bili_llm.json", "r", encoding="utf-8") as file:
    with open("AP_llm.json", "r", encoding="utf-8") as file:
        AP_llm = json.load(file)

    ordered_res_llm = []
    ordered_text = []
    print("Unique GT(LLM) Entries:", len(AP_llm))
    print("Cluster Entries:", len(inputs1))
            
    for index, inp in enumerate(inputs1):
        if(index < 202):
            ordered_text.append(inp)
            ordered_res_llm.append(AP_llm[inputs1[index]])

    print("Combined and ordered. Total Entry:", len(ordered_res_llm))

    llm_zeros = 0
    llm_ones = 0
    for i in range(len(ordered_res_llm)):
        if ordered_res_llm[i] == 0:
            llm_zeros += 1
        else:
            llm_ones += 1

    print("There is", llm_zeros, "zeros and", llm_ones, "ones in Ground Truth(LLM).")

    cluster_zeros = 0
    cluster_ones = 0
    for i in range(len(clusters)):
        if clusters[i] == 0:
            cluster_zeros += 1
        else:
            cluster_ones += 1

    print("There is", cluster_zeros, "zeros and", cluster_ones, "ones in Cluster results(with Deckards).")
            
    cluster_zeros_without_Deckard = 0
    cluster_ones_without_Deckard = 0
    for i in range(0, 202):
        if(clusters[i] == 0):
            cluster_zeros_without_Deckard += 1
        else:
            cluster_ones_without_Deckard += 1
            
    print("There is", cluster_zeros_without_Deckard, "zeros and", cluster_ones_without_Deckard, "ones in Cluster results(without Deckards).")
    Deckard_true_in_zero_cluster = 0
    Deckard_true_in_one_cluster = 0
    for i in range(202, 262):
        if(clusters[i] == 0):
            Deckard_true_in_zero_cluster += 1
        else:
            Deckard_true_in_one_cluster += 1
            
    

    print("Deckard true in zero cluster:", Deckard_true_in_zero_cluster)
    print("Deckard true in one cluster:", Deckard_true_in_one_cluster)
    
    if(Deckard_true_in_zero_cluster > Deckard_true_in_one_cluster):
        print(">>> Cluster 0 is more like the ground truth YES.")
        true_positive = 0
        false_positive = 0
        false_negative = 0
        true_negative = 0

        for i in range(len(ordered_res_llm)):
            if ordered_res_llm[i] == 0 and clusters[i] == 0:
                true_positive += 1
            elif ordered_res_llm[i] == 0 and clusters[i] == 1:
                false_positive += 1
            elif ordered_res_llm[i] == 1 and clusters[i] == 0:
                false_negative += 1
            elif ordered_res_llm[i] == 1 and clusters[i] == 1:
                true_negative += 1
                
        print("True Positive:", true_positive)
        print("False Positive:", false_positive)
        print("False Negative:", false_negative)
        print("True Negative:", true_negative)
        print("Accuracy:", (true_positive + true_negative) / (true_positive + true_negative + false_positive + false_negative))
        
        acc = (true_positive + true_negative) / (true_positive + true_negative + false_positive + false_negative)
    else:
        print(">>> Cluster 1 is more like the ground truth YES.")
        true_positive = 0
        false_positive = 0
        false_negative = 0
        true_negative = 0

        for i in range(len(ordered_res_llm)):
            if ordered_res_llm[i] == 0 and clusters[i] == 1:
                true_positive += 1
            elif ordered_res_llm[i] == 0 and clusters[i] == 0:
                false_positive += 1
            elif ordered_res_llm[i] == 1 and clusters[i] == 0:
                true_negative += 1
            elif ordered_res_llm[i] == 1 and clusters[i] == 1:
                false_negative += 1
                
        print("True Positive:", true_positive)
        print("False Positive:", false_positive)
        print("False Negative:", false_negative)
        print("True Negative:", true_negative)
        print("Accuracy:", (true_positive + true_negative) / (true_positive + true_negative + false_positive + false_negative))
        
        acc = (true_positive + true_negative) / (true_positive + true_negative + false_positive + false_negative)
        
                   
        
    # compare the ordered_res_llm and clusters

    print("--------------------------------")
    return acc

res = {}
for i in range(2, 50):
    res[i] = try_reduce_dim(i)
    

print(res)
