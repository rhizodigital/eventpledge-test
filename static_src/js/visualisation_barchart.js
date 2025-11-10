import * as echarts from "echarts";
let wakeLock = null;

// Detect Safari (desktop or iOS)
const isSafari = /^((?!chrome|android).)*safari/i.test(navigator.userAgent);

export async function requestWakeLock() {
  // Safari or unsupported browser → show warning
  if (isSafari || !("wakeLock" in navigator)) {
    console.warn(
      "⚠️ Wake Lock API not supported in Safari. Please disable auto-lock manually."
    );
    return;
  }

  try {
    // Must be called inside a user gesture (click / touch)
    wakeLock = await navigator.wakeLock.request("screen");
    console.log("✅ Screen Wake Lock is active.");

    // Re-acquire when tab becomes visible again
    document.addEventListener("visibilitychange", async () => {
      if (wakeLock !== null && document.visibilityState === "visible") {
        try {
          wakeLock = await navigator.wakeLock.request("screen");
          console.log("🔄 Wake Lock re-acquired.");
        } catch (err) {
          console.error("Re-acquire failed:", err);
        }
      }
    });
  } catch (err) {
    console.error(`${err.name}: ${err.message}`);
  }
}

document.addEventListener("DOMContentLoaded", () => {
  requestWakeLock();
  const chartDom = document.getElementById("chart");
  const vizContainer = document.getElementById("viz-container");
  if (!chartDom) return;

  const chart = echarts.init(chartDom);

  const normalColor = "#ff425b";
  const highlightColor = "#210c0c";

  function getFontFactor() {
    // The variable cascades globally, so we read it from the root element (<html>).
    const factor = getComputedStyle(vizContainer)
      .getPropertyValue("--viz-font-factor") // Must match the name in the template
      .trim();

    // If factor is empty or invalid, default to 1.0 (100%)
    return parseFloat(factor) || 1.0;
  }
  // Helper function to calculate font size based on viewport width
  function getFontSize() {
    const base = Math.min(window.innerWidth, window.innerHeight);
    // 1.2% of the smaller dimension, min 16px, max 32px
    let size = Math.max(16, Math.min(32, base * 0.016));
    size = size * getFontFactor();
    return size;
  }

  const option = {
    backgroundColor: "transparent",
    grid: {
      left: 40,
      right: 20,
      top: 20,
      bottom: 20,
      containLabel: true,
    },
    xAxis: {
      type: "value",
      axisLabel: { color: "#aaa", fontSize: getFontSize() * 0.8 },
      axisLabel: { show: false }, // hide numbers
      axisLine: { show: false }, // hide the line
      axisTick: { show: false }, // hide tick marks
      splitLine: { show: false }, // hide grid lines
    },
    yAxis: {
      type: "category",
      inverse: true,
      axisLabel: {
        color: "#525252",
        margin: 25,
        fontSize: getFontSize(),
        fontWeight: 700,
        fontFamily: "Inter, sans-serif",
      },
      axisLine: { show: false },
      animationDuration: 300,
      animationDurationUpdate: 300,
    },
    series: [
      {
        type: "bar",
        realtimeSort: true,
        barCategoryGap: "20%",
        barMinHeight: 10,
        label: {
          distance: Math.max(16, Math.min(24, window.innerWidth * 0.01)),
          show: true,
          position: "insideRight",
          color: "#fff",
          fontWeight: 700,
          fontFamily: "Inter, sans-serif",
          fontSize: getFontSize(),
          valueAnimations: true,
          formatter: (params) =>
            params.value > 0 ? params.value.toString() : "",
        },
        data: [],
        itemStyle: {
          color: normalColor,
        },
      },
    ],
    animationDuration: 300,
    animationDurationUpdate: 1000,
    animationEasing: "linear",
    animationEasingUpdate: "linear",
  };

  chart.setOption(option);

  function updateChart(data) {
    const items = Object.entries(data)
      .map(([name, value]) => ({ name, value }))
      .sort((a, b) => b.value - a.value);

    const topName = items.length ? items[0].name : null;

    chart.setOption({
      yAxis: { data: items.map((d) => d.name) },
      series: [
        {
          data: items.map((d) => ({
            name: d.name,
            value: d.value,
            itemStyle: {
              color: d.name === topName ? highlightColor : normalColor,
            },
          })),
        },
      ],
    });
  }

  function updatePledgeFeed(feedData) {
    const feedContainer = document.getElementById("pledge-feed");
    if (!feedContainer) return;

    let newHtml = "";

    feedData.forEach((pledge) => {
      const name = pledge.last_name
        ? `${pledge.first_name} ${pledge.last_name}`
        : pledge.first_name;

      const pledgeHtml = `
        <article class="pledge-entry">
          <blockquote class="pledge-text">${pledge.personal_pledge_censored} <span class="pledge-name">- ${name}</span></blockquote>
          
        </article>
      `;

      feedContainer.insertAdjacentHTML("beforeend", pledgeHtml);
      newHtml += pledgeHtml;
    });
    feedContainer.innerHTML = newHtml;
  }

  updateChart(window.initialCounts || {});
  updatePledgeFeed(window.initialPledgeFeed || []);

  const protocol = window.location.protocol === "https:" ? "wss:" : "ws:";
  const socketPath = `${protocol}//${window.location.host}/ws/live/`;
  const socket = new WebSocket(socketPath);

  socket.onopen = () => {
    console.log("WebSocket connection established.");
  };

  socket.onmessage = (e) => {
    try {
      const data = JSON.parse(e.data);
      // Handle heartbeat
      if (data.type === "heartbeat") {
        console.log("❤️ heartbeat");
        return;
      }

      console.log("Received data:", data);
      const countData = data.counts || {};
      const pledgeFeed = data.pledge_feed || [];

      updateChart(countData);
      updatePledgeFeed(pledgeFeed);
    } catch (error) {
      console.error("Error parsing WebSocket message:", error);
    }
  };

  socket.onclose = (e) => {
    console.warn("WebSocket closed. Reconnecting in 5s...");
    setTimeout(() => {
      window.location.reload(); // simple reconnect
    }, 5000);
  };

  // Dynamically resize font sizes and chart on window resize
  window.addEventListener("resize", () => {
    const fontSize = getFontSize();
    chart.setOption({
      yAxis: { axisLabel: { fontSize: fontSize } },
      series: { label: { fontSize: fontSize } },
    });
    chart.resize();
  });
});
