#!/usr/bin/env python3

# run with taskset to restrict to one core!
# taskset -c 1 ./bench_type_contexts.py

from util import unix_time_bash
import os
import random
import string

US_PER_S = 1000 * 1000
n_records = 1000 * 1000
n_data_points = 10
results_dir = "type_context_results"

def main():
    os.system("rm -fr " + results_dir)
    os.system("mkdir " + results_dir)

    type_range = [x for x in range(0, n_records + 1, int(n_records / n_data_points))]
    type_range[0] = 1 # extreme case is 1 type, not 0
    zson_files = []

    for n_types in type_range:
        f_name = results_dir + "/data_{:0>7}_types.zson".format(n_types)
        zson_files.append((n_types, f_name, open(f_name, "w")))

    for i in range(n_records):
        letter = random.choice(string.ascii_letters)

        for n_types, f_name, f in zson_files:
            if n_types == 1:
                type_name = 0
            else:
                type_name = i % n_types

            f.write("{\"" + "{:0>6}".format(type_name) + "\":\"" + str(letter) + "\"}\n")

    for n_types, f_name, f in zson_files:
        f.close()

    # create zng files
    for n_types, f_name, f in zson_files:
        zng_name = f_name.split(".")[0] + ".zng"
        os.system("zq -f zng -o " + zng_name + " " + f_name)

    # benchmark how long it takes to count all the types in each zng file, etc.
    with open(results_dir + "/results.csv", "w") as f_results:
        f_results.write("query,n_types,real,user,sys,us_per_type\n")
        for n_types, f_name, f in zson_files:
            zng_name = f_name.split(".")[0] + ".zng"

            # count types
            results = unix_time_bash("zq -Z \"by typeof(.) | count()\" " + zng_name)
            fields = ["by typeof count", n_types, results['real'], results['user'], results['sys'],
                      "{:.2f}".format(results['real'] * US_PER_S / n_types)]
            f_results.write(",".join(str(x) for x in fields) + "\n")

            # count records
            results = unix_time_bash("zq -Z \"count()\" " + zng_name)
            fields = ["count", n_types, results['real'], results['user'], results['sys'],
                      "{:.2f}".format(results['real'] * US_PER_S / n_types)]
            f_results.write(",".join(str(x) for x in fields) + "\n")

if __name__ == '__main__':
    main()
