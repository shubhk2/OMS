$(function () {
  var grade = {
    series: [5368, 3500, 4106],
    labels: ["5368", "Refferal Traffic", "Oragnic Traffic"],
    chart: {
      height: 170,
      type: "donut",
      fontFamily: "Plus Jakarta Sans', sans-serif",
      foreColor: "#c6d1e9",
    },

    tooltip: {
      theme: "dark",
      fillSeriesColor: false,
    },

    colors: ["#e7ecf0", "#fb977d", "var(--bs-primary)"],
    dataLabels: {
      enabled: false,
    },

    legend: {
      show: false,
    },

    stroke: {
      show: false,
    },
    responsive: [
      {
        breakpoint: 991,
        options: {
          chart: {
            width: 150,
          },
        },
      },
    ],
    plotOptions: {
      pie: {
        donut: {
          size: '80%',
          background: "none",
          labels: {
            show: true,
            name: {
              show: true,
              fontSize: "12px",
              color: undefined,
              offsetY: 5,
            },
            value: {
              show: false,
              color: "#98aab4",
            },
          },
        },
      },
    },
  };

  var chart = new ApexCharts(document.querySelector("#grade"), grade);
  chart.render();
  var leave = {
    series: [5368, 3500, 4106],
    labels: ["5368", "Unpaid Leave", "Paid Leave"],
    chart: {
      height: 170,
      type: "donut",
      fontFamily: "Plus Jakarta Sans', sans-serif",
      foreColor: "#c6d1e9",
    },

    tooltip: {
      theme: "dark",
      fillSeriesColor: false,
    },

    colors: ["#e7ecf0", "#fb977d", "var(--bs-primary)"],
    dataLabels: {
      enabled: false,
    },

    legend: {
      show: false,
    },

    stroke: {
      show: false,
    },
    responsive: [
      {
        breakpoint: 991,
        options: {
          chart: {
            width: 150,
          },
        },
      },
    ],
    plotOptions: {
      pie: {
        donut: {
          size: '80%',
          background: "none",
          labels: {
            show: true,
            name: {
              show: true,
              fontSize: "12px",
              color: undefined,
              offsetY: 5,
            },
            value: {
              show: false,
              color: "#98aab4",
            },
          },
        },
      },
    },
  };

  var chart1 = new ApexCharts(document.querySelector("#leave"), leave);
  chart1.render();
});