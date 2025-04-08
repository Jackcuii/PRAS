

# import html2txt
# import segment


# dp = [6,7,22,38,41,49,56,61,62,65,80,82,90,93,101,102,104,105,110,111,112,139,192,210,215,218,223,225,238,248]

# for i in dp:
    #html2txt.convert_html_to_text(f"./dataset/original/{i}.html", f"./dataset/text/{i}.txt")
    #segment.segment(f"./dataset/text/{i}.txt", f"./dataset/seged/{i}.txt")

# 线索化数据 就是把各级标题一直贯穿下来.
# 缺少类错误




gdprs = [
    "Personal data shall be processed lawfully, fairly and in a transparent manner in relation to the data subject (‘lawfulness, fairness and transparency’).",
    "Personal data shall be collected for specified, explicit and legitimate purposes and not further processed in a manner that is incompatible with those purposes; further processing for archiving purposes in the public interest, scientific or historical research purposes or statistical purposes shall, in accordance with Article 89(1), not be considered to be incompatible with the initial purposes (‘purpose limitation’).",
    "Personal data shall be adequate, relevant and limited to what is necessary in relation to the purposes for which they are processed (‘data minimisation’).",
    "Personal data shall be accurate and, where necessary, kept up to date; every reasonable step must be taken to ensure that personal data that are inaccurate, having regard to the purposes for which they are processed, are erased or rectified without delay (‘accuracy’).",
    "Personal data shall be kept in a form which permits identification of data subjects for no longer than is necessary for the purposes for which the personal data are processed; personal data may be stored for longer periods insofar as the personal data will be processed solely for archiving purposes in the public interest, scientific or historical research purposes or statistical purposes in accordance with Article 89(1) subject to implementation of the appropriate technical and organisational measures required by this Regulation in order to safeguard the rights and freedoms of the data subject (‘storage limitation’).",
    "Personal data shall be processed in a manner that ensures appropriate security of the personal data, including protection against unauthorised or unlawful processing and against accidental loss, destruction or damage, using appropriate technical or organisational measures (‘integrity and confidentiality’)."
]




if __name__ == "__main__":
    # Load the model and tokenizer
    from llm import load_model
    from llm import ask_model
    load_model()
    
    print("Checking LLM...")
    demo_user_input = "What is the capital of France?"
    print("User: ", demo_user_input)
    response = ask_model(demo_user_input)
    print(response)
    print("LLM check complete.")
    
    print("\n\n")
    
    # load all text data ({n}_genex_total.txt) from all the files in /dataset/dp (n = 1-30)

    import os
    import json
    
    data_dir = "./dataset/dp"
    all_data = []
    
    for x in range(1, 31):
        with open(os.path.join(data_dir, f"{x}_genex_total.txt"), "r") as f:
            all_data.append(f.read().split("\n"))
            
    # load ground truth ({n}_genex_pos.txt) from all the files in /dataset/dp (n = 1-30)
    
    all_gts = []
    for x in range(1, 31):
        with open(os.path.join(data_dir, f"{x}_genex_total_pos.txt"), "r") as f:
            line_sum = len(all_data[x-1])
            gt_pos = f.read().split(",")
            assert len(gt_pos) == 10
            gt_pos = [int(x) for x in gt_pos]
            #if x == 1:
                #[print(all_data[x-1][i]) for i in gt_pos]
            gt = []
            for i in range(line_sum):
                if i in gt_pos:
                    gt.append(1)
                else:
                    gt.append(0)
            all_gts.append(gt)
            
    
    results = []
    count = []
    result_dict = {}
    accuracies = []
    overall_accuracy = 0
    total_false_positive = 0
    total_false_negative = 0
    total_true_positive = 0
    total_true_negative = 0
    
    from judge import start_court, compare_result
    for i in range(len(all_data)):
        result = start_court(all_data[i], gdprs, all_gts[i])
        results.append(result)
        count += [compare_result(results[i], all_gts[i])]
        print(f"The {i+1}th result: ")
        print(f"False Positive: {count[i][0]}, False Negative: {count[i][1]}, True Positive: {count[i][2]}, True Negative: {count[i][3]}")
        accuracy = (count[i][2] + count[i][3]) / (count[i][0] + count[i][1] + count[i][2] + count[i][3])
        overall_accuracy += accuracy
        total_false_positive += count[i][0]
        total_false_negative += count[i][1]
        total_true_positive += count[i][2]
        total_true_negative += count[i][3]
        result_dict[f"{i+1}_genex_total.txt"] = {
            "result": result[i],
            "accuracy": accuracies[i],
            "false_positive": count[i][0],
            "false_negative": count[i][1],
            "true_positive": count[i][2],
            "true_negative": count[i][3]
        }
        # overwrite the result.json
        with open("./result.json", "w") as f:
            json.dump(result_dict, f)
        
        
    print(f"Overall accuracy: {overall_accuracy / len(count)}")
    print(f"Total false positive: {total_false_positive}, Total false negative: {total_false_negative}, Total true positive: {total_true_positive}, Total true negative: {total_true_negative}")
    
    # save result to ./result.json, includes file name, all result,accuracy, false positive, false negative, true positive, true negative
    