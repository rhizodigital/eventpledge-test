import * as echarts from "echarts";

document.addEventListener("DOMContentLoaded", () => {
  const chartDom = document.getElementById("chart");
  if (!chartDom) return;

  const chart = echarts.init(chartDom);

  const normalColor = "#ff425b";
  const highlightColor = "#210c0c";

  // Helper function to calculate font size based on viewport width
  function getFontSize() {
    const base = Math.min(window.innerWidth, window.innerHeight);
    // 1.2% of the smaller dimension, min 16px, max 32px
    return Math.max(16, Math.min(32, base * 0.016));
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

  updateChart(window.initialCounts || {});

  const ws = new WebSocket(`ws://${window.location.host}/ws/live/`);
  ws.onmessage = (e) => {
    const newData = JSON.parse(e.data);
    updateChart(newData);
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
