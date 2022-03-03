import sys
from subprocess import check_output
import os
import csv
import threading


def remove_grade(s):
    s = s[:s.rfind('\n')]
    return s[:s.rfind('\n')] + '\n'


class Mythread(threading.Thread):
    def __init__(self, sid):
        super(Mythread, self).__init__()
        self.sid = sid
        self.score = None
        self.script = self.get_base_script()
        self.log = 'code not found or name error\n'

    def run(self):
        print 'Executing student {}\'s code...'.format(self.sid)
        log_file = open(os.path.join('student_log', '{}.txt'.format(self.sid)), 'w')
        self.script += ['autograder.py', '-S', 'searchAgents.py,student_code/{}_hw1.py'.format(self.sid)]
        if os.path.isfile(os.path.join('student_code', '{}_hw1.py'.format(self.sid))):
            self.get_log_and_score()
        else:
            self.score = [self.sid] + ['0'] * 4 + ['-1']
        log_file.write(self.log)
        log_file.close()
        print 'Finish grading student {}.'.format(self.sid)

    def join(self, *args):
        threading.Thread.join(self)
        return self.score

    def get_log_and_score(self):
        # print threading.current_thread().getName() + '\n'
        out = check_output(self.script)
        self.score = out.splitlines()[-1].split(',')
        total = sum(map(int, self.score[1:]))
        self.score.append(str(total))
        self.log = remove_grade(out)

    def get_base_script(self):
        is_win = sys.platform.startswith('win')
        if is_win:
            script = ['py', '-2']
        else:
            script = ['python2']
        return script


def parallel_grading(student_list):
    thread_list = []
    sorted_unique_student_list = sorted(list(set(student_list)))
    for student_id in sorted_unique_student_list:
        student_id = student_id.strip()
        if student_id:
            t = Mythread(student_id)
            t.setDaemon(True)
            thread_list.append(t)
            t.start()
    return thread_list


def init_csv(csv_name='grade.csv'):
    if not os.path.isfile(csv_name):
        with open(csv_name, 'wb') as csv_file:
            csv.writer(csv_file).writerow(
                ['Student ID', 'Problem1', 'Problem2', 'Problem3', 'Problem4', 'Total Points'])
    with open(csv_name, 'r') as csv_file:
        return list(csv.reader(csv_file))


def main():
    csv_rows = init_csv('grade.csv')
    if len(sys.argv) < 2:
        csv_rows = csv_rows[:1]
        with open('student_list.txt', 'r') as student_list_file:
            thread_list = parallel_grading(student_list_file.read().splitlines())
        for thread in thread_list:
            grade_score = thread.join()
            csv_rows.append(grade_score)
    else:
        thread_list = parallel_grading(sys.argv[1:])
        for thread in thread_list:
            grade_score = thread.join()
            grade_exist = False
            for row in csv_rows[1:]:
                if row[0] == grade_score[0]:
                    grade_exist = True
                    print 'Student {} :'.format(row[0])
                    print 'Old grade : ' + ', '.join(row)
                    print 'New grade : ' + ', '.join(grade_score)
                    if int(grade_score[-1]) > int(row[-1]):
                        print 'Update {}\'s total grade from {}  to {}'.format(row[0], row[-1], grade_score[-1])
                        row[1:] = grade_score[1:]
                    else:
                        print 'New grade is equal or lower than old grade'
            if not grade_exist:
                print 'Append {}\'s grade : '.format(grade_score[0])
                print ', '.join(grade_score)
                csv_rows.append(grade_score)
            print
    with open('grade.csv', 'wb+') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(csv_rows)


if __name__ == '__main__':
    main()
