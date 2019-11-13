#
# Copyright 2019 Delphix
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

# pylint: disable=missing-docstring

import argparse
from typing import Iterable

import drgn
import sdb


class DslDir():

    @staticmethod
    def name(dd):
        pname = ''
        if dd.dd_parent:
            pname = DslDir.name(dd.dd_parent) + '/'
        return pname + dd.dd_myname.string_().decode("utf-8")


class Dataset():

    @staticmethod
    def name(ds):
        if not ds:
            return 'MOS'
        name = DslDir.name(ds.ds_dir)
        if not ds.ds_prev:
            sn = ds.ds_snapname.string_().decode("utf-8")
            if len(sn) == 0:
                sn = '%UNKNOWN_SNAP_NAME%'
            name += '@' + sn
        return name


class Objset():

    @staticmethod
    def name(os):
        return Dataset.name(os.os_dsl_dataset)


class Dbuf(sdb.Locator, sdb.PrettyPrinter):

    names = ["dbuf"]
    input_type = "dmu_buf_impl_t *"
    output_type = "dmu_buf_impl_t *"

    def _init_argparse(self, parser: argparse.ArgumentParser) -> None:
        parser.add_argument(
            '-o',
            '--object',
            type=int,
            help='filter: only dbufs of this object')
        parser.add_argument(
            '-l',
            '--level',
            type=int,
            help='filter: only dbufs of this level')
        parser.add_argument(
            '-b',
            '--blkid',
            type=int,
            help='filter: only dbufs of this blkid')
        parser.add_argument(
            '-d',
            '--dataset',
            type=str,
            help='filter: only dbufs of this dataset name (or "MOS")')
        parser.add_argument(
            '-H',
            '--has-holds',
            action='store_true',
            help='filter: only dbufs that have nonzero holds')

    def pretty_print(self, dbufs):
        print("{:>20} {:>8} {:>4} {:>8} {:>5} {}".format(
            "addr", "object", "lvl", "blkid", "holds", "os"))
        for dbuf in dbufs:
            print("{:>20} {:>8d} {:>4d} {:>8d} {:>5d} {}".format(
                hex(dbuf),
                int(dbuf.db.db_object),
                int(dbuf.db_level),
                int(dbuf.db_blkid),
                int(dbuf.db_holds.rc_count),
                Objset.name(dbuf.db_objset)))

    def filter(self, db):
        if self.args.object and db.db.db_object != self.args.object:
            return False
        if self.args.level and db.db_level != self.args.level:
            return False
        if self.args.blkid and db.db_blkid != self.args.blkid:
            return False
        if self.args.has_holds and db.db_holds.rc_count == 0:
            return False
        if self.args.dataset and Objset.name(db.db_objset) != self.args.dataset:
            return False
        return True

    def no_input(self) -> Iterable[drgn.Object]:
        hash_map = self.prog["dbuf_hash_table"].address_of_()
        for i in range(hash_map.hash_table_mask):
            dbuf = hash_map.hash_table[i]
            while dbuf:
                if self.filter(dbuf):
                    yield dbuf
                dbuf = dbuf.db_hash_next
