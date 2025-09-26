from datetime import timedelta
import json

def parse_time(time):
    h, m, s = map(int, time.split(':'))
    return timedelta(hours=h, minutes=m, seconds=s)

def get_partitions(data, n=5):
    for comment in data:
        comment['timestamp'] = parse_time(comment['time_elapsed'])

    first_comment = min(data, key=lambda x: x['timestamp'])
    last_comment = max(data, key=lambda x: x['timestamp'])
    total_time = last_comment['timestamp'] - first_comment['timestamp']

    partition_size = total_time / n

    partitions = {}

    for index in range(n):
        partitions[index] = {
            'comments': [],
            'start': first_comment['timestamp'] + partition_size * index,
            'end': first_comment['timestamp'] + partition_size * (index + 1)
        }
    
    for comment in data:
        for index, partition in partitions.items():
            if partition['start'] <= comment['timestamp'] < partition['end']:
                partition['comments'].append(comment)

    for index, partition in partitions.items():
        print(f'Partition {index+1}')
        print(f'Comments: {len(partition["comments"])}')
        print(f'Start: {partition["start"]}')
        print(f'End: {partition["end"]}')
        print()
        
    return partitions

    
#if __name__ == '__main__':
#    get_partitions('data.json')