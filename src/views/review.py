"""Answer key and R coverage - the review surfaces."""

from __future__ import annotations

import streamlit as st

from .. import loader, ui


def answer_key(bank):
    st.subheader("Answer key")
    st.caption(
        "Every question with its correct answers, model answer and source slide. "
        "Use this to check the bank, and to revise after a practice session."
    )
    controls = st.columns([2, 2, 3])
    with controls[0]:
        lec = st.selectbox(
            "Lecture", [0] + list(loader.LECTURES),
            format_func=lambda n: "All lectures" if n == 0 else "Lecture %d" % n,
        )
    with controls[1]:
        qtype = st.selectbox("Type", ["All", loader.MC, loader.WA],
                             format_func=lambda s: {"All": "All"}.get(s, s))
    with controls[2]:
        only_flagged = st.checkbox("Only show flagged questions", value=False)

    pool = [q for q in bank if (lec == 0 or q["lecture"] == lec)
            and (qtype == "All" or q["type"] == qtype)]
    if only_flagged:
        flagged = st.session_state.get("flagged", set())
        pool = [q for q in pool if q["id"] in flagged]

    st.caption("%d questions shown" % len(pool))
    if st.session_state.get("flagged"):
        st.caption("Flagged for correction: %s"
                   % ", ".join(sorted(st.session_state["flagged"])))

    for q in pool:
        flagged = q["id"] in st.session_state.get("flagged", set())
        label = "%s %s  [%s]%s" % (
            q["id"], q["topic"][:44], q["type"], "  **FLAGGED**" if flagged else "")
        with st.expander(label):
            ui.render_stem(q, show_source=True)
            if q.get("image"):
                ui.render_figure(q)
            if q["type"] == loader.MC:
                for k, text in q["options"].items():
                    mark = "**[x]**" if k in q["correct"] else "[ ]"
                    st.markdown("%s **%s)** %s" % (mark, k, text))
                st.markdown("**Explanation:** %s" % q["explanation"])
            else:
                st.markdown("**Model answer:**")
                st.markdown(q["answer"])
                if q.get("detail"):
                    # Already inside an expander, so the detail has to be inline:
                    # Streamlit does not allow nested expanders.
                    st.markdown("**Longer explanation:**")
                    st.markdown(q["detail"])
                st.markdown("**Checklist:**")
                for item in q["rubric"]:
                    st.markdown("- %s" % item["text"])
            if st.button("Flag for correction", key="flag_%s" % q["id"]):
                flags = st.session_state.setdefault("flagged", set())
                if q["id"] in flags:
                    flags.discard(q["id"])
                else:
                    flags.add(q["id"])
                st.rerun()

    if st.button("Reset all progress and flags", type="secondary"):
        st.session_state["flagged"] = set()
        st.success("Flags cleared.")


def r_coverage(bank):
    st.subheader("R coverage")
    st.caption(
        "Every R function and package concept that appears in the lectures, and the "
        "questions that test it. Use this to confirm nothing from the course was "
        "skipped."
    )
    funcs = {}
    for q in bank:
        for fn in q.get("r_functions", []):
            funcs.setdefault(fn, []).append(q)

    st.markdown("**%d distinct R functions / concepts** covered across %d questions."
                % (len(funcs), sum(len(v) for v in funcs.values())))
    by_lec = {}
    for fn, qs in funcs.items():
        for q in qs:
            by_lec.setdefault(q["lecture"], set()).add(fn)

    rows = []
    for lec in range(1, 10):
        fset = sorted(by_lec.get(lec, []))
        rows.append((lec, len(fset), ", ".join(fset) if fset else "_none yet_"))
    st.table(
        [{"Lecture": l, "Lecture topic": loader.LECTURES[l], "R functions tested": c,
          "Detail": d}
         for l, c, d in rows]
    )

    st.markdown("**Per function**")
    for fn in sorted(funcs):
        qs = funcs[fn]
        ids = ", ".join(q["id"] for q in qs)
        st.markdown("- `%s` &mdash; %d question(s): %s" % (fn, len(qs), ids))