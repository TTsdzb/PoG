import argparse
from utils import prepare_dataset_for_eval

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--dataset", type=str, default="grailqa", help="choose the dataset."
    )
    parser.add_argument(
        "--output_file",
        type=str,
        default="PoG_grailqa_gpt-3.5-turbo-0125",
        help="the output file name.",
    )
    args = parser.parse_args()

    ground_truth_datas, question_string, output_datas = prepare_dataset_for_eval(
        args.dataset, args.output_file
    )

    with open(f"../PoG/{args.output_file}.csv", mode="w", encoding="utf-8") as csv_file:
        csv_file.write("line,call_num,total_token,input_token,output_token,time")
        for i, data in enumerate(output_datas):
            csv_file.write(
                f"\n{i + 1},{data['call_num']},{data['total_token']},{data['input_token']},{data['output_token']},{data['time']:.02f}"
            )
