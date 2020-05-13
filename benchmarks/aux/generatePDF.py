import pathlib

import numpy as np
import matplotlib.pyplot as plt

from jinja2 import Environment, FileSystemLoader
import lhapdf

# ==========
# globals
# ==========


here = pathlib.Path(__file__).parent.absolute()
env = Environment(loader=FileSystemLoader(str(here / "templatePDF")))


def stringify(ls, fmt="%.6e"):
    return " ".join([fmt % x for x in ls])


def stringify2(ls):
    table = ""
    for line in ls:
        table += ("% .8e " % line[0]) + stringify(line[1:], fmt="%.8e") + "\n"
    return table


# ==========
# dump
# ==========


def dump_pdf(name, xgrid, Q2grid, pids, pdf_table):
    # collect data

    data = dict(
        xgrid=stringify(xgrid),
        Q2grid=stringify(Q2grid),
        pids=stringify(pids, fmt="%d"),
        pdf_table=stringify2(pdf_table),
    )

    # ===========
    # apply template

    templatePDF = env.get_template("templatePDF.dat")
    stream = templatePDF.stream(data)
    stream.dump(str(here / "PDFs" / name / f"{name}_0000.dat"))


def dump_info(name, description, pids):
    # collect data

    data = dict(description=description, pids=pids,)

    # ===========
    # apply template

    templatePDF = env.get_template("templatePDF.info")
    stream = templatePDF.stream(data)
    stream.dump(str(here / "PDFs" / name / f"{name}.info"))


# ==========
# PDFs
# ==========


def uonly():
    name = "uonly"
    (here / "PDFs" / name).mkdir(exist_ok=True)

    # make PDF.dat
    xgrid = np.unique(np.concatenate([np.logspace(-9, 0, 100)]))
    Q2grid = np.logspace(0.3, 5, 20)
    pids = [-3, -2, -1, 1, 2, 3, 21]
    antis = antiu = antid = d = s = g = [0.0 for x in xgrid for Q2 in Q2grid]
    u = [(1.0 - x) * x for x in xgrid for Q2 in Q2grid]
    pdf_table = np.array([antis, antiu, antid, d, u, s, g]).T
    # pdf_table = np.vstack([np.array(pdf_table_Q2).T for i in range(len(Q2grid))])
    dump_pdf(name, xgrid, Q2grid, pids, pdf_table)

    # make PDF.info
    description = "'up quark only PDFset, for debug purpose'"
    dump_info(name, description, pids)

def uonly_dense():
    name = "uonly-dense"
    (here / "PDFs" / name).mkdir(exist_ok=True)

    # make PDF.dat
    xgrid = np.unique(np.concatenate([np.logspace(-9, 0, 100),np.linspace(.8, 1.0, 100)]))
    Q2grid = np.logspace(0.3, 5, 20)
    pids = [-3, -2, -1, 1, 2, 3, 21]
    antis = antiu = antid = d = s = g = [0.0 for x in xgrid for Q2 in Q2grid]
    u = [(1.0 - x) * x for x in xgrid for Q2 in Q2grid]
    pdf_table = np.array([antis, antiu, antid, d, u, s, g]).T
    # pdf_table = np.vstack([np.array(pdf_table_Q2).T for i in range(len(Q2grid))])
    dump_pdf(name, xgrid, Q2grid, pids, pdf_table)

    # make PDF.info
    description = "'up quark only PDFset, for debug purpose, denser in high x'"
    dump_info(name, description, pids)


def gonly():
    name = "gonly"
    (here / "PDFs" / name).mkdir(exist_ok=True)

    # make PDF.dat

    xgrid = np.logspace(-9, 0, 100)
    Q2grid = np.logspace(0.3, 5, 20)
    pids = [-3, -2, -1, 1, 2, 3, 21]
    antis = antiu = antid = d = u = s = [0.0 for x in xgrid for Q2 in Q2grid]
    g = [(1.0 - x) * x for x in xgrid for Q2 in Q2grid]
    pdf_table = np.array([antis, antiu, antid, d, u, s, g]).T
    # pdf_table = np.vstack([np.array(pdf_table_Q2).T for i in range(len(Q2grid))])
    dump_pdf(name, xgrid, Q2grid, pids, pdf_table)

    # make PDF.info
    description = "'gluon only PDFset, for debug purpose'"
    dump_info(name, description, pids)

def check(pdfset,pid):
    pdf = lhapdf.mkPDF(pdfset,0)
    f = lambda x: x*(1.0-x)
    xs = np.logspace(-8, -.2, 100)*(1. + .5*np.random.rand(100))
    #xs = np.array([.1,.5,.8])
    xs = np.unique(xs)
    other = [pdf.xfxQ2(pid,x,10.0) for x in xs]
    ref = f(xs)
    #print(xs)
    #print(other/ref)
    plt.title(pdfset)
    plt.plot(xs, (other-ref)/ref)
    plt.show()


if __name__ == "__main__":
    #uonly_dense()
    #gonly()
    check("uonly",2)
    check("uonly-dense",2)
    check("gonly",21)
