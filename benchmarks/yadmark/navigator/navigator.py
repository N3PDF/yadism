# -*- coding: utf-8 -*-
from banana import navigator

class NavigatorApp(navigator.NavigatorApp):
    """
    Navigator base class holding all elementry operations.

    Parameters
    ----------
        cfg : dict
            banana configuration
        mode : string
            mode identifier
    """

    def fill_theories(self, theo, obj):
        """
        Collect important information of all theories.

        Returns
        -------
            df : pandas.DataFrame
                created frame
        """
        for f in ["PTO", "XIF", "XIR", "TMC", "NfFF", "FNS", "DAMP"]:
            obj[f] = theo[f]

    # def list_all_observables(self):
    #     """
    #     Collect important information of all observables.

    #     Returns
    #     -------
    #         df : pandas.DataFrame
    #             created frame
    #     """
    #     # collect
    #     obs = self.get(o)
    #     data = []
    #     for ob in obs:
    #         obj = {"doc_id": ob.doc_id}
    #         if "PTO" in ob:
    #             obj["PTO"] = ob["PTO"]
    #         xgrid = ob["interpolation_xgrid"]
    #         obj["xgrid"] = (
    #             f"{len(xgrid)}pts: "
    #             + f"{'log' if ob['interpolation_is_log'] else 'x'}"
    #             + f"^{ob['interpolation_polynomial_degree']}"
    #         )
    #         if "prDIS" in ob:
    #             obj["curr"] = ob["prDIS"]
    #         if "projectile" in ob:
    #             proj_map = {
    #                 "electron": "e-",
    #                 "positron": "e+",
    #                 "neutrino": "ν",
    #                 "antineutrino": "ν~",
    #             }
    #             obj["proj"] = proj_map[ob["projectile"]]
    #         if "PolarizationDIS" in ob:
    #             obj["pol"] = ob["PolarizationDIS"]
    #         sfs = 0
    #         esfs = 0
    #         for sf in ob:
    #             # quick fix
    #             if not on.ObservableName.is_valid(sf):
    #                 continue
    #             sfs += 1
    #             esfs += len(ob[sf])
    #         obj["structure_functions"] = f"{sfs} SF @ {esfs} points"
    #         dt = datetime.fromisoformat(ob["_created"])
    #         obj["created"] = human_dates(dt)
    #         data.append(obj)
    #     # output
    #     df = pd.DataFrame(data)
    #     return df

    # def list_all_sim_logs(self, ref_log_or_id):
    #     """
    #     Search logs which are similar to the one given, i.e., same theory and/or same observable.

    #     Parameters
    #     ----------
    #         ref_log_or_id : dict or int
    #             if int doc_id of log to be loaded

    #     Returns
    #     -------
    #         df : pandas.DataFrame
    #             created frame
    #     """
    #     if isinstance(ref_log_or_id, int):
    #         ref_log = self.get(l, ref_log_or_id)
    #     else:
    #         ref_log = ref_log_or_id
    #     rel_logs = []
    #     all_logs = self.get(l)
    #     for lg in all_logs:
    #         if (
    #             "_theory_doc_id" in ref_log
    #             and lg["_theory_doc_id"] != ref_log["_theory_doc_id"]
    #         ):
    #             continue
    #         if (
    #             "_observables_doc_id" in ref_log
    #             and lg["_observables_doc_id"] != ref_log["_observables_doc_id"]
    #         ):
    #             continue
    #         rel_logs.append(lg)
    #     return self.list_all_logs(rel_logs)

    # def list_all_logs(self, logs=None):
    #     """
    #     Collect important information of all logs

    #     Parameters
    #     ----------
    #         logs : list or None
    #             if None plot all

    #     Returns
    #     -------
    #         df : pandas.DataFrame
    #             created frame
    #     """
    #     # collect
    #     if logs is None:
    #         logs = self.get(l)
    #     data = []
    #     for lg in logs:
    #         obj = {"doc_id": lg.doc_id}
    #         sfs = 0
    #         esfs = 0
    #         for sf in lg:
    #             if not on.ObservableName.is_valid(sf):
    #                 continue
    #             sfs += 1
    #             esfs += len(lg[sf])
    #         crash = lg.get("_crash", None)
    #         if crash is None:
    #             obj["structure_functions"] = f"{sfs} SF @ {esfs} pts"
    #         else:
    #             obj["structure_functions"] = crash
    #         obj["theory"] = lg["_theory_doc_id"]
    #         obj["obs"] = lg["_observables_doc_id"]
    #         if "_pdf" in lg:
    #             obj["pdf"] = lg["_pdf"]
    #         if "_creation_time" in lg:
    #             dt = datetime.fromisoformat(lg["_creation_time"])
    #             obj["created"] = human_dates(dt)
    #         data.append(obj)
    #     # output
    #     df = pd.DataFrame(data)
    #     return df

    # def get_log_DFdict(self, doc_id):
    #     """
    #     Load all structure functions in log as DataFrame

    #     Parameters
    #     ----------
    #         doc_id : int
    #             document identifier

    #     Returns
    #     -------
    #         log : DFdict
    #             DataFrames
    #     """
    #     log = self.get(l, doc_id)
    #     dfd = DFdict()
    #     for sf in log:
    #         if not on.ObservableName.is_valid(sf):
    #             continue
    #         dfd.print(
    #             f"{sf} with theory={log['_theory_doc_id']}, "
    #             + f"obs={log['_observables_doc_id']} "
    #             + f"using {log['_pdf']}"
    #         )
    #         dfd[sf] = pd.DataFrame(log[sf])
    #     return dfd

    # def list_all(self, table):
    #     """
    #     List wrapper.

    #     Parameters
    #     ----------
    #         table : str
    #             table name to query: short cut or plural

    #     Returns
    #     -------
    #         df : pandas.DataFrame
    #             created frame
    #     """
    #     if table == t:
    #         return self.list_all_theories()
    #     elif table == o:
    #         return self.list_all_observables()
    #     elif table == l:
    #         return self.list_all_logs()
    #     else:
    #         print(f"Unkown table: {table}")
    #         return []

    # def subtract_tables(self, dfd1, dfd2):
    #     """
    #     Subtract results in the second table from the first one,
    #     properly propagate the integration error and recompute the relative
    #     error on the subtracted results.

    #     Parameters
    #     ----------
    #         dfd1 : dict or int
    #             if int the doc_id of the log to be loaded
    #         dfd2 : dict or int
    #             if int the doc_id of the log to be loaded

    #     Returns
    #     -------
    #         diffout : DFdict
    #             created frames
    #     """

    #     diffout = DFdict()

    #     # load json documents
    #     logs = []
    #     ids = []
    #     for dfd in [dfd1, dfd2]:
    #         if isinstance(dfd, int):
    #             logs.append(self.get(l, dfd))
    #             ids.append(dfd)
    #         elif isinstance(dfd, DFdict):
    #             logs.append(dfd.to_document())
    #             ids.append("not-an-id")
    #         else:
    #             raise ValueError("subtract_tables: DFList not recognized!")
    #     log1, log2 = logs[0], logs[1]
    #     id1, id2 = ids[0], ids[1]

    #     # print head
    #     msg = f"Subtracting id:{id1} - id:{id2}, in table 'logs'"
    #     diffout.print(msg, "=" * len(msg), sep="\n")
    #     diffout.print()

    #     if log1 is None:
    #         raise ValueError(f"Log id:{id1} not found")
    #     if log2 is None:
    #         raise ValueError(f"Log id:{id2} not found")

    #     # iterate observables
    #     for obs in log1.keys():
    #         if obs[0] == "_":
    #             continue
    #         if obs not in log2:
    #             print(f"{obs}: not matching in log2")
    #             continue

    #         # load observable tables
    #         table1 = pd.DataFrame(log1[obs])
    #         table2 = pd.DataFrame(log2[obs])
    #         table_out = table2.copy()

    #         # check for compatible kinematics
    #         if any([any(table1[y] != table2[y]) for y in ["x", "Q2"]]):
    #             raise ValueError("Cannot compare tables with different (x, Q2)")

    #         # subtract and propagate
    #         known_col_set = set(["x", "Q2", "yadism", "yadism_error", "rel_err[%]"])
    #         t1_ext = list(set(table1.keys()) - known_col_set)[0]
    #         t2_ext = list(set(table2.keys()) - known_col_set)[0]
    #         if t1_ext == t2_ext:
    #             tout_ext = t1_ext
    #         else:
    #             tout_ext = f"{t2_ext}-{t1_ext}"
    #         table_out.rename(columns={t2_ext: tout_ext}, inplace=True)
    #         table_out[tout_ext] = table2[t2_ext] - table1[t1_ext]
    #         # subtract our values
    #         table_out["yadism"] -= table1["yadism"]
    #         table_out["yadism_error"] += table1["yadism_error"]

    #         # compute relative error
    #         def rel_err(row, tout_ext=tout_ext):
    #             if row[tout_ext] == 0.0:
    #                 if row["yadism"] == 0.0:
    #                     return 0.0
    #                 return np.nan
    #             else:
    #                 return (row["yadism"] / row[tout_ext] - 1.0) * 100

    #         table_out["rel_err[%]"] = table_out.apply(rel_err, axis=1)

    #         # dump results' table
    #         diffout.print(obs, "-" * len(obs), sep="\n")
    #         diffout[obs] = table_out

    #     return diffout

    # def join(self, id1, id2):
    #     tabs = []
    #     tabs1 = []
    #     exts = []
    #     suffixes = (f" ({id1})", f" ({id2})")

    #     for i, doc_id in enumerate([id1, id2]):
    #         tabs += [self.get_log_DFdict(doc_id)[0]]
    #         tabs1 += [tabs[i].drop(["yadism", "yadism_error", "rel_err[%]"], axis=1)]
    #         exts += [
    #             tabs1[i].columns.drop(["x", "Q2"])[0]
    #         ]  # + suffixes[i]] # TODO the suffixes are not working as expected

    #     def rel_err(row):
    #         ref = row[exts[0]]
    #         cmp = row[exts[1]]
    #         if ref != 0:
    #             return (cmp / ref - 1) * 100
    #         else:
    #             return np.nan

    #     tab_joint = tabs1[0].merge(
    #         tabs1[1], on=["x", "Q2"], how="outer", suffixes=suffixes
    #     )
    #     tab_joint["ext_rel_err [%]"] = tab_joint.apply(rel_err, axis=1)

    #     if all(np.isclose(tabs[0]["yadism"], tabs[1]["yadism"])):
    #         tab_joint["yadism"] = tabs[0]["yadism"]
    #         tab_joint["yadism_error"] = tabs[0]["yadism_error"]
    #     else:
    #         pass

    #     return tab_joint
