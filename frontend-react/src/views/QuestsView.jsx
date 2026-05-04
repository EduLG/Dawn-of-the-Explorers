// src/views/QuestsView.jsx
import { useState, useEffect, useCallback } from "react";
import { useOutletContext } from "react-router-dom";
import { apiFetch } from "../utils/apiFetch";
import useDungeons from "../hooks/useDungeons";

function formatDuration(seconds) {
  if (seconds < 60) return `${seconds}s`;
  const mins = Math.round(seconds / 60);
  return `${mins} min`;
}

function formatTimeLeft(seconds) {
  if (seconds <= 0) return "0s";
  if (seconds < 60) return `${seconds}s`;
  const mins = Math.floor(seconds / 60);
  const secs = seconds % 60;
  return secs > 0 ? `${mins}m ${secs}s` : `${mins}m`;
}

const QuestsView = () => {
  const { party } = useOutletContext();
  const { dungeons, loading, error } = useDungeons();
  const partyRating = party?.rating ?? 0;

  const [activeExploration, setActiveExploration] = useState(null);
  const [timeLeft, setTimeLeft] = useState(0);
  const [exploreResult, setExploreResult] = useState(null);
  const [sending, setSending] = useState(false);

  const applyStatus = useCallback((data) => {
    if (data.status === "in_progress") {
      setActiveExploration((prev) => {
        const newEndsAt = new Date(data.ends_at);
        if (prev?.ends_at?.getTime() === newEndsAt.getTime()) return prev;
        return { ends_at: newEndsAt, dungeon_name: data.dungeon_name };
      });
    } else if (data.status === "completed") {
      setActiveExploration(null);
      setExploreResult({
        success: data.success,
        loot: data.loot,
        dungeonName: data.dungeon_name,
      });
    } else {
      setActiveExploration(null);
    }
  }, []);

  useEffect(() => {
    apiFetch("/api/v1/dungeons/exploration/status")
      .then((r) => r.json())
      .then(applyStatus)
      .catch(() => {});
  }, [applyStatus]);

  useEffect(() => {
    if (!activeExploration) {
      setTimeLeft(0);
      return;
    }
    const tick = () => {
      const diff = Math.ceil(
        (activeExploration.ends_at.getTime() - Date.now()) / 1000,
      );
      const remaining = Math.max(0, diff);
      setTimeLeft(remaining);
      if (remaining === 0) {
        apiFetch("/api/v1/dungeons/exploration/status")
          .then((r) => r.json())
          .then(applyStatus)
          .catch(() => {});
      }
    };
    tick();
    const id = setInterval(tick, 1000);
    return () => clearInterval(id);
  }, [activeExploration, applyStatus]);

  const handleSend = async (dungeon) => {
    setSending(true);
    try {
      const res = await apiFetch(`/api/v1/dungeons/${dungeon.id}/explore`, {
        method: "POST",
      });
      const data = await res.json();
      applyStatus(data);
    } catch {
      /* ignore */
    } finally {
      setSending(false);
    }
  };

  const busy = !!activeExploration || sending;

  return (
    <>
      {/* Header */}
      <div
        className="border rounded-2xl px-6 py-4 flex flex-col sm:flex-row sm:items-center sm:justify-between gap-3"
        style={{
          background: "var(--bg-card)",
          borderColor: "var(--border-soft)",
        }}
      >
        <div>
          <h2
            className="text-xl sm:text-2xl font-bold"
            style={{ color: "var(--text-primary)" }}
          >
            Exploration Quests
          </h2>
        </div>
        <div className="flex flex-col items-start sm:items-end gap-0.5">
          <span
            className="text-xs uppercase tracking-widest"
            style={{ color: "var(--text-muted)" }}
          >
            Party Rating
          </span>
          <span
            className="text-2xl font-bold"
            style={{ color: "var(--accent)" }}
          >
            {partyRating}
          </span>
        </div>
      </div>

      {/* Active exploration banner */}
      {activeExploration && (
        <div
          className="rounded-xl px-5 py-4 border flex items-center justify-between gap-4"
          style={{
            background: "var(--status-blue-bg)",
            borderColor: "var(--status-blue-border)",
          }}
        >
          <div>
            <p
              className="text-[10px] uppercase tracking-widest mb-0.5"
              style={{ color: "var(--status-blue-text)" }}
            >
              Exploring
            </p>
            <p
              className="text-sm font-semibold"
              style={{ color: "var(--text-primary)" }}
            >
              {activeExploration.dungeon_name}
            </p>
          </div>
          <span
            className="text-2xl font-bold tabular-nums"
            style={{ color: "var(--accent)" }}
          >
            {formatTimeLeft(timeLeft)}
          </span>
        </div>
      )}

      {/* Explore result banner */}
      {exploreResult && (
        <div
          className="rounded-xl px-5 py-4 border flex flex-col gap-3"
          style={
            exploreResult.success
              ? {
                  background: "var(--status-green-bg)",
                  borderColor: "var(--status-green-border)",
                }
              : {
                  background: "var(--status-red-bg)",
                  borderColor: "var(--status-red-border)",
                }
          }
        >
          <div className="flex items-center justify-between gap-4">
            <div>
              <p
                className="text-[10px] uppercase tracking-widest mb-0.5"
                style={{
                  color: exploreResult.success
                    ? "var(--status-green-text)"
                    : "var(--status-red-text)",
                }}
              >
                {exploreResult.success
                  ? "Exploration successful"
                  : "Exploration failed"}
              </p>
              <p
                className="text-sm font-semibold"
                style={{ color: "var(--text-primary)" }}
              >
                {exploreResult.dungeonName}
              </p>
            </div>
            <button
              onClick={() => setExploreResult(null)}
              className="text-xs transition-colors shrink-0"
              style={{ color: "var(--text-muted)" }}
            >
              Dismiss
            </button>
          </div>
          {exploreResult.success && exploreResult.loot.length > 0 && (
            <div className="flex flex-wrap gap-2">
              {exploreResult.loot.map((item) => (
                <span
                  key={item.id}
                  className="text-[11px] rounded-lg px-3 py-1 border"
                  style={{
                    background: "var(--bg-tag)",
                    borderColor: "var(--border-soft)",
                    color: "var(--text-primary)",
                  }}
                >
                  {item.name}
                  <span className="ml-1.5" style={{ color: "var(--accent)" }}>
                    +{item.rating}
                  </span>
                </span>
              ))}
            </div>
          )}
        </div>
      )}

      {/* Loading / error */}
      {loading && (
        <p
          className="text-sm text-center py-8"
          style={{ color: "var(--text-muted)" }}
        >
          Loading dungeons...
        </p>
      )}
      {error && (
        <p
          className="text-sm text-center py-8"
          style={{ color: "var(--status-red-text)" }}
        >
          Failed to load dungeons.
        </p>
      )}

      {/* Dungeons grid */}
      {!loading && !error && (
        <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-4 sm:gap-5">
          {dungeons.map((dungeon) => {
            const ratingOk = partyRating >= dungeon.min_rating;
            let buttonLabel;
            let buttonStyle;
            if (busy) {
              buttonLabel = activeExploration ? "Party is away" : "Sending...";
              buttonStyle = {
                background: "var(--bg-input)",
                borderColor: "var(--border-faint)",
                color: "var(--text-disabled)",
                cursor: "not-allowed",
              };
            } else if (!ratingOk) {
              buttonLabel = `Requires ${dungeon.min_rating} rating`;
              buttonStyle = {
                background: "var(--bg-input)",
                borderColor: "var(--border-faint)",
                color: "var(--text-disabled)",
                cursor: "not-allowed",
              };
            } else {
              buttonLabel = "Send Party";
              buttonStyle = {
                background: "var(--accent-dim)",
                borderColor: "var(--accent-border)",
                color: "var(--text-primary)",
                cursor: "pointer",
              };
            }

            return (
              <div
                key={dungeon.id}
                className="flex flex-col rounded-2xl overflow-hidden border transition-all duration-200"
                style={{
                  background: "var(--bg-card)",
                  borderColor: "var(--border-soft)",
                }}
              >
                {/* Cover image */}
                <div className="relative h-44 overflow-hidden shrink-0">
                  <img
                    src={dungeon.image_path}
                    alt={dungeon.name}
                    className="w-full h-full object-cover transition-transform duration-500 hover:scale-105"
                  />
                  <div className="absolute inset-0 bg-gradient-to-t from-black/70 via-black/10 to-transparent" />
                  <span
                    className="absolute top-2.5 right-2.5 text-[10px] bg-black/60 px-2 py-0.5 rounded-full"
                    style={{ color: "var(--text-muted)" }}
                  >
                    {formatDuration(dungeon.duration)}
                  </span>
                  {dungeon.min_rating > 0 && (
                    <span
                      className="absolute bottom-2.5 right-2.5 text-[10px] bg-black/60 px-2 py-0.5 rounded-full"
                      style={{ color: "var(--text-muted)" }}
                    >
                      Min. {dungeon.min_rating}
                    </span>
                  )}
                </div>

                {/* Card body */}
                <div className="flex flex-col flex-1 p-4 gap-3">
                  <h3
                    className="text-sm font-bold leading-snug"
                    style={{ color: "var(--text-primary)" }}
                  >
                    {dungeon.name}
                  </h3>
                  <p
                    className="text-xs leading-relaxed flex-1"
                    style={{ color: "var(--text-secondary)" }}
                  >
                    {dungeon.description}
                  </p>
                  <button
                    onClick={() => handleSend(dungeon)}
                    disabled={busy || !ratingOk}
                    className="mt-2 w-full py-2 rounded-xl text-xs font-semibold uppercase tracking-wider transition-all duration-200 border"
                    style={buttonStyle}
                  >
                    {buttonLabel}
                  </button>
                </div>
              </div>
            );
          })}
        </div>
      )}
    </>
  );
};

export default QuestsView;
