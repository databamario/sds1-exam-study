"""Progress dashboard."""

from __future__ import annotations

import streamlit as st

from .. import loader, progress


def dashboard(bank, conn):
    st.subheader("Progress")
    overall = progress.overall(conn)
    if overall["attempts"] == 0:
        st.info("No attempts recorded yet. Do a practice session or a mock exam.")
        return

    pct = (overall["got"] / overall["possible"] * 100) if overall["possible"] else 0.0
    c1, c2, c3 = st.columns(3)
    c1.metric("Attempts", overall["attempts"])
    c2.metric("Points", "%.1f / %.1f" % (overall["got"], overall["possible"]))
    c3.metric("Score", "%.0f%%" % pct)

    rows = progress.by_lecture(conn)
    st.markdown("**By lecture**")
    st.table([
        {
            "Lecture": r["lecture"],
            "Type": r["qtype"],
            "Questions seen": r["n"],
            "Points": "%.1f / %.1f" % (r["got"], r["poss"]),
        }
        for r in rows
    ])

    st.markdown("**Weakest areas**")
    weak = [r for r in rows if r["poss"] and (r["got"] / r["poss"]) < 0.7]
    if weak:
        for r in sorted(weak, key=lambda r: r["got"] / r["poss"]):
            st.markdown("- Lecture %d (%s): %.0f%%"
                        % (r["lecture"], r["qtype"],
                           100 * r["got"] / r["poss"]))
    else:
        st.success("No lecture is below 70% yet.")

    st.divider()
    if st.button("Reset all progress", type="secondary"):
        progress.reset(conn)
        st.success("Progress cleared.")
        st.rerun()