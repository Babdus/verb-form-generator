import sys
from collections import defaultdict

import pandas as pd


def main(args):
    file_path = args[0]
    df = pd.read_csv(file_path)
    # print(df.describe())
    # print(df.head())
    # print(df.columns)
    df['combined_index'] = df['verb_ids'].astype(str) + '_' + df['screeve_ids'] + '_' + df['subject_numbers'] + '_' + df['subject_persons'] + '_' + df['object_numbers'] + '_' + df['object_persons']
    df.set_index('combined_index', inplace=True)
    # print(df.head())

    counter = 0

    percentage_dict = defaultdict(list)

    for row in df.itertuples():
        if row.preverb_ids != '{NULL}':
            continue
        # print(row)
        v, s, sn, sp, on, op = row.Index.split('_')
        # print(v, s, sn, sp, on, op)
        # print(row.paired_screeve_ids)
        to_be_found_index = '_'.join((v, row.paired_screeve_ids, sn, sp, on, op))
        # print(to_be_found_index)
        if to_be_found_index in df.index:
            found_row = df.loc[[to_be_found_index]]
            # print(found_row)
            with_preverb_count = sum(found_row['concordance_count'])
            # print(with_preverb_count)
            without_preverb_count = row.concordance_count
            # print(without_preverb_count)
            if with_preverb_count + without_preverb_count == 0:
                fraction = None
            else:
                fraction = with_preverb_count / (without_preverb_count + with_preverb_count)
            # print(fraction)
            if fraction is not None:
                percentage_dict[row.blueprint_ids[1:-1]].append(
                    {'v': v, 's': s, 'sn': s, 'sp': s, 'on': on, 'op': op, 'with_preverb_fraction': fraction}
                )
        else:
            percentage_dict[row.blueprint_ids[1:-1]].append({'v': v, 's': s, 'sn': s, 'sp': s, 'on': on, 'op': op, 'with_preverb_fraction': 0.0})

        # print(f'{30 + (counter % 2) * 60 + counter % 8}')
        # print(f'\033[0;{30 + ((counter // 8) % 2) * 60 + counter % 8}m')
        counter += 1
        if counter > 10000:
            break
    print(f'\033[0m')

    for blueprint_id in percentage_dict:
        data = percentage_dict[blueprint_id]
        data.append(sum(row['with_preverb_fraction'] for row in data)/len(data))

    for blueprint_id in percentage_dict:
        print(blueprint_id, end=': ')
        print(percentage_dict[blueprint_id][-1])


if __name__ == '__main__':
    main(sys.argv[1:])