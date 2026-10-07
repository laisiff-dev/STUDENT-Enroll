import json

with open('dashboard_data.json', 'r', encoding='utf-8') as f:
    data_json = f.read()

# We escape JS template literal variables inside python string
html_content = '''<!DOCTYPE html>
<html lang="zh-TW">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>輔英科技大學 - 5年招生歷程與生源變化戰情與決策系統 (111~115學年度)</title>
    <!-- Chart.js -->
    <script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.1/dist/chart.umd.min.js"></script>
    <!-- FontAwesome Font for Icons -->
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css">
    <!-- Google Fonts -->
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Noto+Sans+TC:wght@400;500;600;700;800;900&family=Outfit:wght@400;500;600;700&display=swap" rel="stylesheet">
    <style>
        :root {
            --bg-body: #f8fafc;
            --bg-card: #ffffff;
            --bg-card-hover: #f1f5f9;
            --bg-control: #f1f5f9;
            --border-color: #cbd5e1;
            --border-light: #e2e8f0;
            
            --text-main: #0f172a;
            --text-muted: #334155;
            --text-dim: #64748b;
            
            --accent-cyan: #0284c7;
            --accent-blue: #2563eb;
            --accent-indigo: #4f46e5;
            --accent-purple: #7c3aed;
            --accent-emerald: #059669;
            --accent-amber: #d97706;
            --accent-rose: #e11d48;
            
            --shadow-sm: 0 2px 8px rgba(15, 23, 42, 0.06);
            --shadow-md: 0 4px 16px rgba(15, 23, 42, 0.08);
            --shadow-lg: 0 8px 24px rgba(15, 23, 42, 0.12);
        }

        * {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
        }

        body {
            font-family: 'Noto Sans TC', 'Outfit', -apple-system, BlinkMacSystemFont, sans-serif;
            background-color: var(--bg-body);
            color: var(--text-main);
            line-height: 1.6;
            padding: 28px;
            min-height: 100vh;
            font-size: 16px;
        }

        /* Top Header */
        .app-header {
            background: #ffffff;
            border: 1px solid var(--border-color);
            border-radius: 20px;
            padding: 28px 36px;
            margin-bottom: 28px;
            box-shadow: var(--shadow-md);
            display: flex;
            justify-content: space-between;
            align-items: center;
            flex-wrap: wrap;
            gap: 20px;
        }

        .header-title-box h1 {
            font-size: 30px;
            font-weight: 800;
            color: #1e3a8a;
            margin-bottom: 8px;
            display: flex;
            align-items: center;
            gap: 14px;
        }

        .header-title-box p {
            color: var(--text-muted);
            font-size: 16px;
            font-weight: 500;
        }

        .header-tags {
            display: flex;
            gap: 12px;
            flex-wrap: wrap;
        }

        .tag-pill {
            background: #e0f2fe;
            border: 1px solid #bae6fd;
            color: #0284c7;
            padding: 8px 16px;
            border-radius: 30px;
            font-size: 14px;
            font-weight: 700;
            display: flex;
            align-items: center;
            gap: 8px;
        }
        
        .tag-pill.purple {
            background: #f3e8ff;
            border-color: #e9d5ff;
            color: #7c3aed;
        }

        .tag-pill.emerald {
            background: #d1fae5;
            border-color: #a7f3d0;
            color: #059669;
        }

        /* Control Toolbar */
        .control-toolbar {
            background: var(--bg-card);
            border: 1px solid var(--border-color);
            border-radius: 20px;
            padding: 20px 28px;
            margin-bottom: 28px;
            display: flex;
            flex-wrap: wrap;
            align-items: center;
            justify-content: space-between;
            gap: 20px;
            box-shadow: var(--shadow-sm);
        }

        .control-group {
            display: flex;
            align-items: center;
            gap: 12px;
            flex-wrap: wrap;
        }

        .control-label {
            font-size: 15px;
            font-weight: 700;
            color: var(--text-muted);
            text-transform: uppercase;
            letter-spacing: 0.5px;
            margin-right: 4px;
            display: flex;
            align-items: center;
            gap: 8px;
        }

        .btn-option {
            background: var(--bg-control);
            color: var(--text-muted);
            border: 1px solid var(--border-color);
            padding: 10px 18px;
            border-radius: 12px;
            font-size: 15px;
            font-weight: 700;
            cursor: pointer;
            transition: all 0.25s ease;
            display: inline-flex;
            align-items: center;
            gap: 8px;
        }

        .btn-option:hover {
            background: #e2e8f0;
            color: var(--text-main);
            border-color: #94a3b8;
        }

        .btn-option.active {
            background: #2563eb;
            color: #ffffff;
            border-color: #1d4ed8;
            box-shadow: 0 4px 12px rgba(37, 99, 235, 0.25);
        }

        .btn-export {
            background: linear-gradient(135deg, #059669, #10b981);
            color: white;
            border: none;
            padding: 11px 22px;
            border-radius: 12px;
            font-size: 15px;
            font-weight: 800;
            cursor: pointer;
            transition: all 0.25s ease;
            box-shadow: 0 4px 12px rgba(16, 185, 129, 0.25);
            display: inline-flex;
            align-items: center;
            gap: 10px;
        }

        .btn-export:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 18px rgba(16, 185, 129, 0.35);
        }

        /* Navigation Stage Tabs */
        .stage-nav {
            display: flex;
            gap: 14px;
            margin-bottom: 28px;
            overflow-x: auto;
            padding-bottom: 4px;
        }

        .stage-tab {
            background: var(--bg-card);
            border: 1px solid var(--border-color);
            color: var(--text-muted);
            padding: 16px 24px;
            border-radius: 16px;
            font-size: 16px;
            font-weight: 800;
            cursor: pointer;
            transition: all 0.3s ease;
            display: flex;
            align-items: center;
            gap: 12px;
            white-space: nowrap;
            flex: 1;
            justify-content: center;
            box-shadow: var(--shadow-sm);
        }

        .stage-tab:hover {
            background: var(--bg-card-hover);
            color: var(--text-main);
            border-color: #94a3b8;
        }

        .stage-tab.active {
            background: #ffffff;
            border: 2px solid #2563eb;
            color: #1d4ed8;
            box-shadow: 0 6px 20px rgba(37, 99, 235, 0.18);
        }

        /* Dynamic Summary Stat Cards */
        .stats-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
            gap: 20px;
            margin-bottom: 28px;
        }

        .stat-card {
            background: var(--bg-card);
            border: 1px solid var(--border-color);
            border-radius: 18px;
            padding: 24px;
            position: relative;
            overflow: hidden;
            transition: all 0.3s ease;
            box-shadow: var(--shadow-sm);
        }

        .stat-card:hover {
            transform: translateY(-4px);
            border-color: #94a3b8;
            box-shadow: var(--shadow-md);
        }

        .stat-card::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            width: 6px;
            height: 100%;
            background: var(--accent-blue);
        }

        .stat-card.purple::before { background: var(--accent-purple); }
        .stat-card.emerald::before { background: var(--accent-emerald); }
        .stat-card.amber::before { background: var(--accent-amber); }
        .stat-card.rose::before { background: var(--accent-rose); }

        .stat-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 14px;
        }

        .stat-title {
            font-size: 15px;
            font-weight: 700;
            color: var(--text-muted);
        }

        .stat-icon {
            width: 44px;
            height: 44px;
            border-radius: 12px;
            background: #f1f5f9;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 20px;
            color: #2563eb;
        }

        .stat-value {
            font-size: 34px;
            font-weight: 900;
            color: var(--text-main);
            font-family: 'Outfit', sans-serif;
            margin-bottom: 6px;
            letter-spacing: -0.5px;
        }

        .stat-desc {
            font-size: 14px;
            color: var(--text-dim);
            display: flex;
            align-items: center;
            gap: 6px;
            font-weight: 500;
        }

        .stat-desc .highlight {
            color: #059669;
            font-weight: 800;
        }

        /* Section Layout Containers */
        .stage-content {
            display: none;
            animation: fadeIn 0.4s ease forwards;
        }

        .stage-content.active {
            display: block;
        }

        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(10px); }
            to { opacity: 1; transform: translateY(0); }
        }

        .grid-2col {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(560px, 1fr));
            gap: 26px;
            margin-bottom: 28px;
        }

        @media (max-width: 768px) {
            .grid-2col {
                grid-template-columns: 1fr;
            }
        }

        /* Component Card (Chart/Table) */
        .component-card {
            background: var(--bg-card);
            border: 1px solid var(--border-color);
            border-radius: 20px;
            padding: 28px;
            margin-bottom: 28px;
            box-shadow: var(--shadow-sm);
            transition: border-color 0.3s ease;
        }

        .component-card:hover {
            border-color: #94a3b8;
            box-shadow: var(--shadow-md);
        }

        .card-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 22px;
            padding-bottom: 16px;
            border-bottom: 2px solid #f1f5f9;
            flex-wrap: wrap;
            gap: 14px;
        }

        .card-title {
            font-size: 20px;
            font-weight: 800;
            color: var(--text-main);
            display: flex;
            align-items: center;
            gap: 12px;
        }

        .card-title i {
            color: #2563eb;
        }

        .card-actions {
            display: flex;
            gap: 10px;
        }

        .btn-card-action {
            background: var(--bg-control);
            border: 1px solid var(--border-color);
            color: var(--text-muted);
            padding: 7px 15px;
            border-radius: 10px;
            font-size: 14px;
            font-weight: 700;
            cursor: pointer;
            transition: all 0.2s ease;
            display: flex;
            align-items: center;
            gap: 6px;
        }

        .btn-card-action:hover {
            background: #cbd5e1;
            color: var(--text-main);
        }

        .chart-wrapper {
            position: relative;
            height: 380px;
            width: 100%;
        }

        /* Analysis Box Inside Cards */
        .analysis-box {
            background: #f8fafc;
            border-left: 5px solid #2563eb;
            border-radius: 0 12px 12px 0;
            padding: 16px 20px;
            margin-top: 20px;
            font-size: 15px;
            border-top: 1px solid var(--border-light);
            border-right: 1px solid var(--border-light);
            border-bottom: 1px solid var(--border-light);
        }

        .analysis-box.emerald { border-left-color: var(--accent-emerald); background: #f0fdf4; }
        .analysis-box.purple { border-left-color: var(--accent-purple); background: #faf5ff; }
        .analysis-box.amber { border-left-color: var(--accent-amber); background: #fffbeb; }

        .analysis-item {
            margin-bottom: 8px;
            display: flex;
            align-items: flex-start;
            gap: 10px;
            color: var(--text-muted);
            font-weight: 500;
        }

        .analysis-item:last-child {
            margin-bottom: 0;
        }

        .badge-tag {
            padding: 4px 10px;
            border-radius: 6px;
            font-size: 12px;
            font-weight: 800;
            white-space: nowrap;
        }

        .badge-quant { background: #e0f2fe; color: #0284c7; }
        .badge-qual { background: #f3e8ff; color: #7c3aed; }
        .badge-strat { background: #d1fae5; color: #059669; }

        /* Tables Styling */
        .table-responsive {
            width: 100%;
            overflow-x: auto;
            border-radius: 14px;
            border: 1px solid var(--border-color);
        }

        .custom-table {
            width: 100%;
            border-collapse: collapse;
            font-size: 15px;
            text-align: left;
        }

        .custom-table th {
            background: #f1f5f9;
            color: #1e293b;
            font-weight: 800;
            padding: 14px 16px;
            border-bottom: 2px solid var(--border-color);
            white-space: nowrap;
        }

        .custom-table td {
            padding: 13px 16px;
            border-bottom: 1px solid var(--border-light);
            color: var(--text-main);
            white-space: nowrap;
        }

        .custom-table tbody tr {
            transition: background 0.2s ease;
        }

        .custom-table tbody tr.row-highlight {
            background: #eff6ff !important;
            font-weight: 700;
        }

        .custom-table tbody tr:hover {
            background: #f8fafc;
        }

        .custom-table tbody tr:last-child td {
            border-bottom: none;
        }

        .badge-highlight {
            background: #d1fae5;
            color: #059669;
            padding: 4px 10px;
            border-radius: 8px;
            font-weight: 800;
        }

        /* Workflow System Architecture Diagram */
        .architecture-diagram {
            background: linear-gradient(135deg, #ffffff 0%, #f8fafc 100%);
            border: 2px solid var(--border-color);
            border-radius: 24px;
            padding: 32px;
            margin-bottom: 28px;
            box-shadow: var(--shadow-sm);
        }

        .flow-steps-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
            gap: 20px;
            position: relative;
            margin-top: 24px;
        }

        .flow-node {
            background: #ffffff;
            border: 2px solid var(--border-color);
            border-radius: 16px;
            padding: 22px;
            text-align: center;
            position: relative;
            transition: all 0.3s ease;
            cursor: pointer;
            box-shadow: var(--shadow-sm);
        }

        .flow-node:hover {
            border-color: #2563eb;
            transform: translateY(-4px);
            box-shadow: var(--shadow-md);
        }

        .flow-node .step-num {
            width: 32px;
            height: 32px;
            border-radius: 50%;
            background: linear-gradient(135deg, #2563eb, #0284c7);
            color: white;
            font-weight: 900;
            font-size: 15px;
            display: flex;
            align-items: center;
            justify-content: center;
            margin: 0 auto 12px auto;
        }

        .flow-node h4 {
            font-size: 16px;
            font-weight: 800;
            margin-bottom: 8px;
            color: var(--text-main);
        }

        .flow-node p {
            font-size: 13px;
            color: var(--text-muted);
            line-height: 1.5;
        }

        /* Hierarchical IR Strategy Sections */
        .hierarchy-section {
            margin-bottom: 28px;
        }

        .hierarchy-header {
            font-size: 20px;
            font-weight: 800;
            color: #1e3a8a;
            margin-bottom: 16px;
            padding-bottom: 10px;
            border-bottom: 2px solid #cbd5e1;
            display: flex;
            align-items: center;
            gap: 12px;
        }

        .strategy-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
            gap: 22px;
        }

        .strategy-card {
            background: var(--bg-card);
            border: 1px solid var(--border-color);
            border-radius: 18px;
            padding: 24px;
            transition: all 0.3s ease;
            box-shadow: var(--shadow-sm);
        }

        .strategy-card:hover {
            border-color: #2563eb;
            transform: translateY(-3px);
            box-shadow: var(--shadow-md);
        }

        .strategy-card.college {
            border-top: 5px solid #2563eb;
        }

        .strategy-card.dept {
            border-top: 5px solid #7c3aed;
        }

        .strategy-card.school {
            border-top: 5px solid #059669;
        }

        .strategy-icon {
            width: 48px;
            height: 48px;
            border-radius: 14px;
            background: #f1f5f9;
            color: #2563eb;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 22px;
            margin-bottom: 16px;
        }

        .strategy-card.dept .strategy-icon {
            color: #7c3aed;
            background: #faf5ff;
        }

        .strategy-card.school .strategy-icon {
            color: #059669;
            background: #f0fdf4;
        }

        .strategy-card h4 {
            font-size: 18px;
            font-weight: 800;
            color: var(--text-main);
            margin-bottom: 10px;
        }

        .strategy-card p {
            font-size: 14px;
            color: var(--text-muted);
            line-height: 1.6;
            font-weight: 500;
        }

        .strategy-card ul {
            padding-left: 20px;
            font-size: 14px;
            color: var(--text-muted);
            line-height: 1.7;
        }

        /* Footer */
        .app-footer {
            text-align: center;
            padding: 28px 0 12px 0;
            color: var(--text-dim);
            font-size: 14px;
            border-top: 1px solid var(--border-color);
            margin-top: 48px;
            font-weight: 500;
        }
    </style>
</head>
<body>

    <!-- Header Section -->
    <header class="app-header">
        <div class="header-title-box">
            <h1><i class="fa-solid fa-chart-line"></i> 輔英科技大學 - 招生歷程與生源變化戰情決策系統</h1>
            <p>近5年 (111~115學年度) 「甄選入學」與「申請入學」階段歷程 ‧ 生源學校消長 ‧ 區域空間轉換 ‧ 動態學年篩選</p>
        </div>
        <div class="header-tags">
            <div class="tag-pill"><i class="fa-solid fa-filter"></i> 招生雙管道勾稽</div>
            <div class="tag-pill purple"><i class="fa-solid fa-school"></i> 動態篩選連動</div>
            <div class="tag-pill emerald"><i class="fa-solid fa-file-export"></i> 圖/表多格式導出</div>
        </div>
    </header>

    <!-- Global Control Toolbar -->
    <div class="control-toolbar">
        <!-- Year Selector -->
        <div class="control-group">
            <span class="control-label"><i class="fa-regular fa-calendar-check"></i> 學年度：</span>
            <button class="btn-option active" data-year="all" onclick="setYearFilter('all')">5年全景 (111-115)</button>
            <button class="btn-option" data-year="115" onclick="setYearFilter('115')">115學年</button>
            <button class="btn-option" data-year="114" onclick="setYearFilter('114')">114學年</button>
            <button class="btn-option" data-year="113" onclick="setYearFilter('113')">113學年</button>
            <button class="btn-option" data-year="112" onclick="setYearFilter('112')">112學年</button>
            <button class="btn-option" data-year="111" onclick="setYearFilter('111')">111學年</button>
        </div>

        <!-- Channel Selector -->
        <div class="control-group">
            <span class="control-label"><i class="fa-solid fa-code-branch"></i> 管道：</span>
            <button class="btn-option active" data-channel="all" onclick="setChannelFilter('all')">全部管道</button>
            <button class="btn-option" data-channel="zhenxuan" onclick="setChannelFilter('zhenxuan')">📘 四技甄選 (技高)</button>
            <button class="btn-option" data-channel="shenqing" onclick="setChannelFilter('shenqing')">📗 四技申請 (普高)</button>
        </div>

        <!-- View Mode Selector -->
        <div class="control-group">
            <span class="control-label"><i class="fa-solid fa-eye"></i> 呈現模式：</span>
            <button class="btn-option active" data-view="chart" onclick="setViewMode('chart')"><i class="fa-solid fa-chart-pie"></i> 統計圖表</button>
            <button class="btn-option" data-view="table" onclick="setViewMode('table')"><i class="fa-solid fa-table"></i> 數據表格</button>
            <button class="btn-option" data-view="both" onclick="setViewMode('both')"><i class="fa-solid fa-table-columns"></i> 圖表併陳</button>
        </div>

        <!-- Export Global Actions -->
        <div class="control-group">
            <button class="btn-export" onclick="exportAllTablesCSV()"><i class="fa-solid fa-file-csv"></i> 匯出全頁表格 (CSV)</button>
        </div>
    </div>

    <!-- DYNAMIC SUMMARY KPI STAT CARDS -->
    <div class="stats-grid">
        <div class="stat-card" id="cardKpi1">
            <div class="stat-header">
                <span class="stat-title" id="kpiTitle1">5年總一階通過人數</span>
                <div class="stat-icon"><i class="fa-solid fa-users"></i></div>
            </div>
            <div class="stat-value" id="kpiValue1">8,492 <span style="font-size:16px">人次</span></div>
            <div class="stat-desc" id="kpiDesc1">甄選 2,632 人次 ‧ 申請 5,860 人次</div>
        </div>

        <div class="stat-card purple" id="cardKpi2">
            <div class="stat-header">
                <span class="stat-title" id="kpiTitle2">5年總正式報到人數</span>
                <div class="stat-icon" style="color:#7c3aed"><i class="fa-solid fa-user-check"></i></div>
            </div>
            <div class="stat-value" id="kpiValue2">1,284 <span style="font-size:16px">人</span></div>
            <div class="stat-desc" id="kpiDesc2">甄選 527 人 ‧ 申請 757 人</div>
        </div>

        <div class="stat-card emerald" id="cardKpi3">
            <div class="stat-header">
                <span class="stat-title" id="kpiTitle3">申請入學就讀轉換率</span>
                <div class="stat-icon" style="color:#059669"><i class="fa-solid fa-arrow-trend-up"></i></div>
            </div>
            <div class="stat-value" id="kpiValue3">32.8%</div>
            <div class="stat-desc" id="kpiDesc3">二階報名 2,310人 ➔ 報到 757人</div>
        </div>

        <div class="stat-card amber" id="cardKpi4">
            <div class="stat-header">
                <span class="stat-title" id="kpiTitle4">甄選入學分發報到率</span>
                <div class="stat-icon" style="color:#d97706"><i class="fa-solid fa-award"></i></div>
            </div>
            <div class="stat-value" id="kpiValue4">95.6%</div>
            <div class="stat-desc" id="kpiDesc4">分發即確定就讀 ‧ 高黏著強意願</div>
        </div>

        <div class="stat-card rose" id="cardKpi5">
            <div class="stat-header">
                <span class="stat-title" id="kpiTitle5">高屏在地生源就讀比率</span>
                <div class="stat-icon" style="color:#e11d48"><i class="fa-solid fa-location-dot"></i></div>
            </div>
            <div class="stat-value" id="kpiValue5">60.6%</div>
            <div class="stat-desc" id="kpiDesc5">5年累計 778 人 ‧ 地利扎根核心</div>
        </div>
    </div>

    <!-- Navigation Tabs for Logical Workflow Stages -->
    <nav class="stage-nav">
        <button class="stage-tab active" data-stage="stage0" onclick="switchStage('stage0')">
            <i class="fa-solid fa-sitemap"></i> 系統流程架構圖與邏輯說明
        </button>
        <button class="stage-tab" data-stage="stage1" onclick="switchStage('stage1')">
            <i class="fa-solid fa-filter-circle-dollar"></i> (1) 招生管道漏斗與階段歷程
        </button>
        <button class="stage-tab" data-stage="stage2" onclick="switchStage('stage2')">
            <i class="fa-solid fa-school-flag"></i> (2) 近5年生源學校與區域變化
        </button>
        <button class="stage-tab" data-stage="stage3" onclick="switchStage('stage3')">
            <i class="fa-solid fa-diagram-project"></i> (3) 分層 IR 招生對策 (學院/系所/全校)
        </button>
    </nav>

    <!-- STAGE 0: System Architecture & Workflow Logic -->
    <div id="stage0" class="stage-content active">
        <div class="architecture-diagram">
            <div class="card-header" style="border-bottom:none; padding-bottom:0;">
                <div class="card-title"><i class="fa-solid fa-diagram-next"></i> 系統數據處理與邏輯順序架構 (System Architecture Workflow)</div>
                <div class="tag-pill emerald"><i class="fa-solid fa-check-double"></i> 依據指定(1)+(2)前後邏輯重構</div>
            </div>
            <p style="color:var(--text-muted); font-size:15px; margin-top:10px;">
                本系統將招生數據處理拆解為四個連續階段，選擇上方「學年度」切換時，全頁數據、KPI卡片與圖表均即時連動過濾：
            </p>

            <div class="flow-steps-grid">
                <div class="flow-node" onclick="switchStage('stage1')">
                    <div class="step-num">1</div>
                    <h4>入學管道階段勾稽</h4>
                    <p>甄選(一階→二階→錄取→報到)<br>申請(一階→二階→報到狀態過濾)</p>
                </div>

                <div class="flow-node" onclick="switchStage('stage2')">
                    <div class="step-num">2</div>
                    <h4>生源學校與區域分析</h4>
                    <p>Top 15 生源學校動態排名<br>6大地理分區空間位移</p>
                </div>

                <div class="flow-node" onclick="switchStage('stage2')">
                    <div class="step-num">3</div>
                    <h4>漏斗轉換與矩陣定位</h4>
                    <p>報名人次 vs 就讀人數轉換率<br>BCG 矩陣定位明星與觀望區</p>
                </div>

                <div class="flow-node" onclick="switchStage('stage3')">
                    <div class="step-num">4</div>
                    <h4>分層 IR 策略與行動導出</h4>
                    <p>學院 / 重點系所 / 全校整體策略<br>圖/表 PNG 與 CSV 多格式導出</p>
                </div>
            </div>
        </div>

        <div class="grid-2col">
            <div class="component-card">
                <div class="card-header">
                    <div class="card-title"><i class="fa-solid fa-list-check"></i> 管道一：四技甄選入學 (技高體系) 階段歷程邏輯</div>
                </div>
                <div style="font-size:15px; color:var(--text-muted);">
                    <ul style="padding-left:22px; line-height:1.8;">
                        <li><b>一階篩選：</b>採統測成績篩選，5年累計 2,632 人次。近 5 年呈緊縮趨勢 (111年 793人次 降至 115年 353人次)。</li>
                        <li><b>二階複試：</b>審查與面試。受南部技高少子化減班衝擊。</li>
                        <li><b>志願錄取：</b>經聯合分發委員會正備取分發至本校。</li>
                        <li><b>實際報到：</b>通過分發後學生<b>報到黏著度極高 (平均 95.6%)</b>，主要流入職安系、保營系、健美系與幼保系。</li>
                    </ul>
                </div>
            </div>

            <div class="component-card">
                <div class="card-header">
                    <div class="card-title"><i class="fa-solid fa-list-check"></i> 管道二：四技申請入學 (普通高中體系) 階段歷程邏輯</div>
                </div>
                <div style="font-size:15px; color:var(--text-muted);">
                    <ul style="padding-left:22px; line-height:1.8;">
                        <li><b>一階篩選：</b>採學測成績篩選，規模穩定維持在 1,000 人次以上。</li>
                        <li><b>二階複試：</b>考生可多校選填與獲多重正備取資格。</li>
                        <li><b>報到狀態過濾：</b>精準勾稽「已確認」與「聯合會已報到」，<b>排除「報到後放棄」(每年 60~100 人)</b>。</li>
                        <li><b>就讀轉換：</b>就讀轉換率從 111年 <b>29.4% 躍升至 115年 41.7% (155人)</b>，護理系 (412人) 與健管系 (86人) 為主力。</li>
                    </ul>
                </div>
            </div>
        </div>
    </div>

    <!-- STAGE 1: Admission Funnel Stages -->
    <div id="stage1" class="stage-content">
        <div class="grid-2col">
            <!-- Chart 1: 甄選入學 Funnel -->
            <div class="component-card card-chart-box">
                <div class="card-header">
                    <div class="card-title" id="titleZhenxuanChart"><i class="fa-solid fa-filter"></i> 四技甄選入學 (技高) 歷年各階段人數消長</div>
                    <div class="card-actions">
                        <button class="btn-card-action" onclick="exportChartImage('chartZhenxuanFunnel', '甄選入學階段人數圖')"><i class="fa-solid fa-camera"></i> PNG</button>
                        <button class="btn-card-action" onclick="exportTableCSVFromData('zhenxuan_funnel', '甄選入學階段數據.csv')"><i class="fa-solid fa-download"></i> CSV</button>
                    </div>
                </div>
                <div class="chart-wrapper">
                    <canvas id="chartZhenxuanFunnel"></canvas>
                </div>
                <div class="analysis-box">
                    <div class="analysis-item"><span class="badge-tag badge-quant">量化</span> 一階篩選通過自 111年 793人次調降至 115年 353人次，實際報到自 161人調整至 78人。</div>
                    <div class="analysis-item"><span class="badge-tag badge-qual">質化</span> 分發錄取後報到意願高達 95.6%，顯示學生選填後對本校黏著度極高。</div>
                </div>
            </div>

            <!-- Chart 2: 申請入學 Funnel -->
            <div class="component-card card-chart-box">
                <div class="card-header">
                    <div class="card-title" id="titleShenqingChart"><i class="fa-solid fa-filter"></i> 四技申請入學 (普高) 歷年各階段人數消長</div>
                    <div class="card-actions">
                        <button class="btn-card-action" onclick="exportChartImage('chartShenqingFunnel', '申請入學階段人數圖')"><i class="fa-solid fa-camera"></i> PNG</button>
                        <button class="btn-card-action" onclick="exportTableCSVFromData('shenqing_funnel', '申請入學階段數據.csv')"><i class="fa-solid fa-download"></i> CSV</button>
                    </div>
                </div>
                <div class="chart-wrapper">
                    <canvas id="chartShenqingFunnel"></canvas>
                </div>
                <div class="analysis-box emerald">
                    <div class="analysis-item"><span class="badge-tag badge-quant">量化</span> 一階維持千人規模，就讀轉換率從 29.4% 攀升至 41.7%，115年報到達 155人。</div>
                    <div class="analysis-item"><span class="badge-tag badge-strat">策略</span> 存在多校重複錄取特性，每年約 60~100 位正取生「報到後放棄」(多流向國北護/長庚科大)，宜加強關懷留存。</div>
                </div>
            </div>
        </div>

        <!-- Table View for Stage 1 -->
        <div class="component-card card-table-box">
            <div class="card-header">
                <div class="card-title"><i class="fa-solid fa-table-list"></i> 兩大入學管道階段歷程統計明細表</div>
                <button class="btn-card-action" onclick="exportTableCSVFromElement('tableStage1All', '兩管道歷程統計表.csv')"><i class="fa-solid fa-file-excel"></i> 匯出表格</button>
            </div>
            <div class="table-responsive">
                <table class="custom-table" id="tableStage1All">
                    <thead>
                        <tr>
                            <th>入學管道</th>
                            <th>學年度</th>
                            <th>一階篩選通過人次(人數)</th>
                            <th>二階報名人次(人數)</th>
                            <th>分發/確認人數</th>
                            <th>最終已報到人數</th>
                            <th>一階→二階報名率</th>
                            <th>錄取/二階→報到就讀率</th>
                        </tr>
                    </thead>
                    <tbody id="tbodyStage1">
                    </tbody>
                </table>
            </div>
        </div>

        <!-- Department Level Comparison Tables -->
        <div class="grid-2col">
            <div class="component-card">
                <div class="card-header">
                    <div class="card-title"><i class="fa-solid fa-building-columns"></i> 甄選入學 (技高) 各學系報到人數消長</div>
                </div>
                <div class="table-responsive">
                    <table class="custom-table">
                        <thead>
                            <tr>
                                <th>學系名稱</th>
                                <th>111</th>
                                <th>112</th>
                                <th>113</th>
                                <th>114</th>
                                <th>115</th>
                                <th>5年合計</th>
                            </tr>
                        </thead>
                        <tbody id="tbodyZhenxuanDepts"></tbody>
                    </table>
                </div>
            </div>

            <div class="component-card">
                <div class="card-header">
                    <div class="card-title"><i class="fa-solid fa-building-columns"></i> 申請入學 (普高) 各學系報到人數消長</div>
                </div>
                <div class="table-responsive">
                    <table class="custom-table">
                        <thead>
                            <tr>
                                <th>學系名稱</th>
                                <th>111</th>
                                <th>112</th>
                                <th>113</th>
                                <th>114</th>
                                <th>115</th>
                                <th>5年合計</th>
                            </tr>
                        </thead>
                        <tbody id="tbodyShenqingDepts"></tbody>
                    </table>
                </div>
            </div>
        </div>
    </div>

    <!-- STAGE 2: Origin Schools & Regional Changes -->
    <div id="stage2" class="stage-content">
        <div class="grid-2col">
            <!-- Chart 3: Top 15 Enrolled Schools -->
            <div class="component-card card-chart-box">
                <div class="card-header">
                    <div class="card-title" id="titleTop15Chart"><i class="fa-solid fa-school"></i> 近 5 年全校主要生源學校就讀人數 (Top 15)</div>
                    <button class="btn-card-action" onclick="exportChartImage('chartTop15Enrolled', 'Top15生源就讀圖')"><i class="fa-solid fa-camera"></i> PNG</button>
                </div>
                <div class="chart-wrapper">
                    <canvas id="chartTop15Enrolled"></canvas>
                </div>
            </div>

            <!-- Chart 4: Geographic Region Trends -->
            <div class="component-card card-chart-box">
                <div class="card-header">
                    <div class="card-title" id="titleRegionChart"><i class="fa-solid fa-map-location-dot"></i> 近 5 年就讀學生之「生源區域」分佈與變化</div>
                    <button class="btn-card-action" onclick="exportChartImage('chartRegionTrend', '生源區域分佈圖')"><i class="fa-solid fa-camera"></i> PNG</button>
                </div>
                <div class="chart-wrapper">
                    <canvas id="chartRegionTrend"></canvas>
                </div>
            </div>
        </div>

        <!-- BCG Matrix Scatter Chart -->
        <div class="component-card card-chart-box">
            <div class="card-header">
                <div class="card-title" id="titleBCGChart"><i class="fa-solid fa-chart-gantt"></i> 生源學校 BCG 矩陣 (報名規模 vs 就讀轉換率 %)</div>
                <button class="btn-card-action" onclick="exportChartImage('chartBCGMatrix', 'BCG生源轉換矩陣圖')"><i class="fa-solid fa-camera"></i> PNG</button>
            </div>
            <div class="chart-wrapper" style="height:400px;">
                <canvas id="chartBCGMatrix"></canvas>
            </div>
            <div class="analysis-box purple">
                <div class="analysis-item"><span class="badge-tag badge-quant">明星區</span> <b>中山工商</b> (報名400, 就讀101, 轉換率25.3%) 與 <b>小港高中</b> (報名153, 就讀44, 轉換率28.8%) 居核心明星地位。</div>
                <div class="analysis-item"><span class="badge-tag badge-qual">觀望區</span> <b>道明高中</b> (報名190, 就讀25, 13.2%) 與 <b>溪湖高中</b> (報名118, 就讀8, 6.8%) 屬高報名、低轉換之觀望區，跨區交通與獎學金為攔截關鍵。</div>
            </div>
        </div>

        <!-- Top 15 Origin High Schools Table -->
        <div class="component-card card-table-box">
            <div class="card-header">
                <div class="card-title"><i class="fa-solid fa-table"></i> Top 15 生源學校就讀與報名轉換統計明細表</div>
                <button class="btn-card-action" onclick="exportTableCSVFromElement('tableTop15Full', 'Top15生源學校統計表.csv')"><i class="fa-solid fa-file-csv"></i> 匯出 CSV</button>
            </div>
            <div class="table-responsive">
                <table class="custom-table" id="tableTop15Full">
                    <thead>
                        <tr>
                            <th>排名</th>
                            <th>生源學校</th>
                            <th>學校屬性</th>
                            <th>111就讀</th>
                            <th>112就讀</th>
                            <th>113就讀</th>
                            <th>114就讀</th>
                            <th>115就讀</th>
                            <th>就讀小計/合計</th>
                            <th>報名人次</th>
                            <th>就讀轉換率 (%)</th>
                            <th>趨勢與變化型態備註</th>
                        </tr>
                    </thead>
                    <tbody id="tbodyTop15Full"></tbody>
                </table>
            </div>
        </div>

        <!-- Region Distribution Table -->
        <div class="component-card card-table-box">
            <div class="card-header">
                <div class="card-title"><i class="fa-solid fa-map"></i> 歷年生源地理區域 (高屏/南部/中部/北部/東部/離島) 報名 vs 就讀統計表</div>
                <button class="btn-card-action" onclick="exportTableCSVFromElement('tableRegionsFull', '生源區域對照表.csv')"><i class="fa-solid fa-file-csv"></i> 匯出 CSV</button>
            </div>
            <div class="table-responsive">
                <table class="custom-table" id="tableRegionsFull">
                    <thead>
                        <tr>
                            <th>地理分區</th>
                            <th>涵蓋代表縣市</th>
                            <th>報名總人次</th>
                            <th>報名佔比</th>
                            <th>111就讀</th>
                            <th>112就讀</th>
                            <th>113就讀</th>
                            <th>114就讀</th>
                            <th>115就讀</th>
                            <th>就讀小計/合計</th>
                            <th>就讀佔比</th>
                            <th>就讀轉換率 (%)</th>
                        </tr>
                    </thead>
                    <tbody id="tbodyRegionsFull"></tbody>
                </table>
            </div>
        </div>
    </div>

    <!-- STAGE 3: Hierarchical IR Strategy (College -> Department -> School) -->
    <div id="stage3" class="stage-content">
        <!-- 1. 學院層級策略 -->
        <div class="hierarchy-section">
            <div class="hierarchy-header">
                <i class="fa-solid fa-graduation-cap"></i> 一、 學院層級招生定位與策略 (College-Level IR Strategies)
            </div>
            <div class="strategy-grid">
                <div class="strategy-card college">
                    <div class="strategy-icon"><i class="fa-solid fa-user-nurse"></i></div>
                    <h4>醫護學院 (College of Nursing)</h4>
                    <p><b>核心屬性：</b>普高生源絕對主戰場 (申請管道 5年就讀 483人)。</p>
                    <ul style="margin-top:8px;">
                        <li><b>策略要點：</b>強化「高國考通過率」與「附設醫院實習就業一條龍」。</li>
                        <li><b>競合防禦：</b>設立「第一志願早鳥獎學金」，攔截流向國北護與長庚科大之正取考生。</li>
                    </ul>
                </div>

                <div class="strategy-card college">
                    <div class="strategy-icon"><i class="fa-solid fa-flask-vial"></i></div>
                    <h4>環境與生命學院 (College of Environment & Life)</h4>
                    <p><b>核心屬性：</b>技高考照優勢與特色工科 (職安系、環工系、應化系、生技系)。</p>
                    <ul style="margin-top:8px;">
                        <li><b>策略要點：</b>職安系為技高招生第 1 大系 (5年73人)，應深化高雄三大工業區產學合辦專班。</li>
                        <li><b>名額調整：</b>環工與生技系適度將甄選缺額彈性調配至四技申請。</li>
                    </ul>
                </div>

                <div class="strategy-card college">
                    <div class="strategy-icon"><i class="fa-solid fa-heart-pulse"></i></div>
                    <h4>健康產業與管理學院 (College of Health Industry)</h4>
                    <p><b>核心屬性：</b>雙軌並進與急速成長 (健管系、物治系、健美系、幼保系)。</p>
                    <ul style="margin-top:8px;">
                        <li><b>策略要點：</b>健管系普高快速成長 (5年86人)，增加在地社區公立高中宣導。</li>
                        <li><b>技高深耕：</b>健美與幼保系鞏固中山工商與樹德家商核心職科源。</li>
                    </ul>
                </div>
            </div>
        </div>

        <!-- 2. 重點系所對策 -->
        <div class="hierarchy-section">
            <div class="hierarchy-header">
                <i class="fa-solid fa-hospital-user"></i> 二、 重點系所精準行動對策 (Department-Level Action Plans)
            </div>
            <div class="strategy-grid">
                <div class="strategy-card dept">
                    <div class="strategy-icon"><i class="fa-solid fa-syringe"></i></div>
                    <h4>護理系 (Nursing Dept.)</h4>
                    <p><b>數據概況：</b>普高 412人 + 技高 66人 = 5年共 478人就讀。</p>
                    <p style="margin-top:8px;"><b>行動對策：</b>建立二階正取生「報到後放棄」即時關懷預警機制，提供免費優質宿舍保障與高額國考獎學金，鎖定屏女、道明等高流失校。</p>
                </div>

                <div class="strategy-card dept">
                    <div class="strategy-icon"><i class="fa-solid fa-hard-hat"></i></div>
                    <h4>職業安全衛生系 (OSH Dept.)</h4>
                    <p><b>數據概況：</b>技高 73人 (全校技高管道就讀人數最高學系)。</p>
                    <p style="margin-top:8px;"><b>行動對策：</b>強化「高薪工業安全師證照」與「臨海/大社工業區企業預聘入學」，深耕中正高工、高雄高工等工科職校。</p>
                </div>

                <div class="strategy-card dept">
                    <div class="strategy-icon"><i class="fa-solid fa-hands-holding-child"></i></div>
                    <h4>物理治療系 (PT Dept.)</h4>
                    <p><b>數據概況：</b>普高 71人 + 技高 45人 (雙管道發展均衡)。</p>
                    <p style="margin-top:8px;"><b>行動對策：</b>針對中部巨人高中醫護專班及在地小港、潮州高中，提供一對一面試輔導與臨床物理治療體驗營。</p>
                </div>

                <div class="strategy-card dept">
                    <div class="strategy-icon"><i class="fa-solid fa-notes-medical"></i></div>
                    <h4>健康事業管理系 (Healthcare Admin)</h4>
                    <p><b>數據概況：</b>普高 86人 (申請管道第 2 大系)。</p>
                    <p style="margin-top:8px;"><b>行動對策：</b>結合智慧醫療大數據課程特色，主打醫院行政管理高就業率，吸引文山、左營等社區公立普高。</p>
                </div>
            </div>
        </div>

        <!-- 3. 全校整體策略 -->
        <div class="hierarchy-section">
            <div class="hierarchy-header">
                <i class="fa-solid fa-building-flag"></i> 三、 全校整體 IR 招生戰略方針 (University-Wide Holistic IR Strategy)
            </div>
            <div class="strategy-grid">
                <div class="strategy-card school">
                    <div class="strategy-icon"><i class="fa-solid fa-tree-city"></i></div>
                    <h4>1. 扎根在地公立普高</h4>
                    <p>深耕小港、潮州、林園、岡山等高就讀意願核心校，實施常態微課程對接、高中導師與輔導室深度拜訪。</p>
                </div>

                <div class="strategy-card school">
                    <div class="strategy-icon"><i class="fa-solid fa-hand-holding-dollar"></i></div>
                    <h4>2. 跨區早鳥獎學金與補貼</h4>
                    <p>鎖定道明、溪湖、屏女、屏中等「高報名低轉換」觀望校，提供第一志願早鳥獎學金與面試交通住宿補貼。</p>
                </div>

                <div class="strategy-card school">
                    <div class="strategy-icon"><i class="fa-solid fa-arrow-right-arrow-left"></i></div>
                    <h4>3. 名額動態滾動調配</h4>
                    <p>順應生源由技高向普高位移趨勢，適度將甄選縮減名額流用至四技申請入學 (尤其是護理、物治、健管系)。</p>
                </div>

                <div class="strategy-card school">
                    <div class="strategy-icon"><i class="fa-solid fa-user-clock"></i></div>
                    <h4>4. 正取流失實時關懷</h4>
                    <p>建立申請入學二階正取生「報到後放棄」即時關懷機制，提供優質宿舍與就業保障訊息，及時攔截學生。</p>
                </div>
            </div>
        </div>

        <!-- Cross Channel Comparison Table -->
        <div class="component-card card-table-box">
            <div class="card-header">
                <div class="card-title"><i class="fa-solid fa-code-compare"></i> 四技甄選入學 (技高) vs 四技申請入學 (普高) 深度二元交叉對比</div>
            </div>
            <div class="table-responsive">
                <table class="custom-table">
                    <thead>
                        <tr>
                            <th>地理區域 / 比較項目</th>
                            <th>【四技甄選入學】(技高體系)</th>
                            <th>【四技申請入學】(普通高中體系)</th>
                            <th>二元結構差異與決策解析</th>
                        </tr>
                    </thead>
                    <tbody id="tbodyCrossGeo"></tbody>
                </table>
            </div>
        </div>
    </div>

    <!-- Footer -->
    <footer class="app-footer">
        <p>輔英科技大學 招生戰情決策系統 ‧ Data Powered by 校務研究與招生數據庫 (111~115學年度)</p>
    </footer>

    <!-- JavaScript Application Logic with Full Reactive Filters -->
    <script>

        // Embed raw structured JSON
        const DASHBOARD_DATA = {
  "zhenxuan_funnel": [
    {
      "year": "111",
      "p1_pass_cnt": 793,
      "p1_pass_people": 725,
      "p2_apply_cnt": 422,
      "p2_apply_people": 422,
      "admitted": 171,
      "enrolled": 161,
      "p1_to_p2_rate": "58.2%",
      "admitted_to_enrolled_rate": "94.2%"
    },
    {
      "year": "112",
      "p1_pass_cnt": 531,
      "p1_pass_people": 482,
      "p2_apply_cnt": 230,
      "p2_apply_people": 230,
      "admitted": 100,
      "enrolled": 93,
      "p1_to_p2_rate": "47.7%",
      "admitted_to_enrolled_rate": "93.0%"
    },
    {
      "year": "113",
      "p1_pass_cnt": 556,
      "p1_pass_people": 461,
      "p2_apply_cnt": null,
      "p2_apply_people": null,
      "admitted": 114,
      "enrolled": 109,
      "p1_to_p2_rate": "—",
      "admitted_to_enrolled_rate": "95.6%"
    },
    {
      "year": "114",
      "p1_pass_cnt": 399,
      "p1_pass_people": 360,
      "p2_apply_cnt": 162,
      "p2_apply_people": 162,
      "admitted": 86,
      "enrolled": 86,
      "p1_to_p2_rate": "45.0%",
      "admitted_to_enrolled_rate": "100.0%"
    },
    {
      "year": "115",
      "p1_pass_cnt": 353,
      "p1_pass_people": 353,
      "p2_apply_cnt": 162,
      "p2_apply_people": 162,
      "admitted": null,
      "enrolled": 78,
      "p1_to_p2_rate": "45.9%",
      "admitted_to_enrolled_rate": "—"
    }
  ],
  "zhenxuan_depts": [
    {
      "dept": "職業安全衛生系",
      "y111": 10,
      "y112": 11,
      "y113": 22,
      "y114": 9,
      "y115": 21,
      "total": 73
    },
    {
      "dept": "護理系",
      "y111": 44,
      "y112": 11,
      "y113": 1,
      "y114": 5,
      "y115": 5,
      "total": 66
    },
    {
      "dept": "保健營養系",
      "y111": 12,
      "y112": 11,
      "y113": 17,
      "y114": 10,
      "y115": 9,
      "total": 59
    },
    {
      "dept": "健康美容系",
      "y111": 18,
      "y112": 11,
      "y113": 9,
      "y114": 9,
      "y115": 10,
      "total": 57
    },
    {
      "dept": "幼兒保育暨產業系",
      "y111": 15,
      "y112": 12,
      "y113": 10,
      "y114": 8,
      "y115": 7,
      "total": 52
    },
    {
      "dept": "物理治療系",
      "y111": 11,
      "y112": 14,
      "y113": 8,
      "y114": 9,
      "y115": 3,
      "total": 45
    },
    {
      "dept": "休閒與遊憩事業管理系",
      "y111": 14,
      "y112": 5,
      "y113": 15,
      "y114": 8,
      "y115": 1,
      "total": 43
    },
    {
      "dept": "高齡及長期照護事業系",
      "y111": 17,
      "y112": 5,
      "y113": 5,
      "y114": 7,
      "y115": 4,
      "total": 38
    },
    {
      "dept": "資訊科技與管理系",
      "y111": 9,
      "y112": 5,
      "y113": 2,
      "y114": 8,
      "y115": 2,
      "total": 26
    },
    {
      "dept": "環境工程與科學系",
      "y111": 4,
      "y112": 1,
      "y113": 7,
      "y114": 3,
      "y115": 9,
      "total": 24
    },
    {
      "dept": "應用化學及材料科學系",
      "y111": 4,
      "y112": 3,
      "y113": 7,
      "y114": 5,
      "y115": 4,
      "total": 23
    },
    {
      "dept": "健康事業管理系",
      "y111": 2,
      "y112": 1,
      "y113": 4,
      "y114": 3,
      "y115": 2,
      "total": 12
    },
    {
      "dept": "生物科技與綠色產業系 (含原生科系)",
      "y111": 0,
      "y112": 3,
      "y113": 0,
      "y114": 2,
      "y115": 1,
      "total": 6
    },
    {
      "dept": "應用外語系",
      "y111": 1,
      "y112": 0,
      "y113": 2,
      "y114": 0,
      "y115": 0,
      "total": 3
    }
  ],
  "shenqing_funnel": [
    {
      "year": "111",
      "p1_pass_cnt": 1349,
      "p1_pass_people": 1228,
      "p2_apply_cnt": 656,
      "p2_apply_people": 606,
      "confirmed": 193,
      "joint_enrolled": null,
      "final_enrolled": 193,
      "p2_to_enrolled_rate": "29.4%"
    },
    {
      "year": "112",
      "p1_pass_cnt": 1282,
      "p1_pass_people": 1129,
      "p2_apply_cnt": 505,
      "p2_apply_people": 463,
      "confirmed": 148,
      "joint_enrolled": 148,
      "final_enrolled": 148,
      "p2_to_enrolled_rate": "29.3%"
    },
    {
      "year": "113",
      "p1_pass_cnt": 1085,
      "p1_pass_people": 960,
      "p2_apply_cnt": 382,
      "p2_apply_people": 352,
      "confirmed": 126,
      "joint_enrolled": 126,
      "final_enrolled": 126,
      "p2_to_enrolled_rate": "33.0%"
    },
    {
      "year": "114",
      "p1_pass_cnt": 1083,
      "p1_pass_people": 957,
      "p2_apply_cnt": 395,
      "p2_apply_people": 360,
      "confirmed": 133,
      "joint_enrolled": 135,
      "final_enrolled": 135,
      "p2_to_enrolled_rate": "34.2%"
    },
    {
      "year": "115",
      "p1_pass_cnt": 1061,
      "p1_pass_people": 929,
      "p2_apply_cnt": 372,
      "p2_apply_people": 345,
      "confirmed": 155,
      "joint_enrolled": 155,
      "final_enrolled": 155,
      "p2_to_enrolled_rate": "41.7%"
    }
  ],
  "shenqing_depts": [
    {
      "dept": "護理系",
      "y111": 91,
      "y112": 90,
      "y113": 70,
      "y114": 77,
      "y115": 84,
      "total": 412
    },
    {
      "dept": "健康事業管理系",
      "y111": 25,
      "y112": 12,
      "y113": 15,
      "y114": 20,
      "y115": 14,
      "total": 86
    },
    {
      "dept": "物理治療系",
      "y111": 13,
      "y112": 15,
      "y113": 13,
      "y114": 15,
      "y115": 15,
      "total": 71
    },
    {
      "dept": "環境工程與科學系",
      "y111": 24,
      "y112": 11,
      "y113": 1,
      "y114": 8,
      "y115": 14,
      "total": 58
    },
    {
      "dept": "應用化學及材料科學系",
      "y111": 16,
      "y112": 6,
      "y113": 14,
      "y114": 3,
      "y115": 8,
      "total": 47
    },
    {
      "dept": "生物科技與綠色產業系 (含原生科系)",
      "y111": 16,
      "y112": 11,
      "y113": 5,
      "y114": 4,
      "y115": 7,
      "total": 43
    },
    {
      "dept": "健康美容系",
      "y111": 8,
      "y112": 3,
      "y113": 3,
      "y114": 1,
      "y115": 6,
      "total": 21
    },
    {
      "dept": "幼兒保育暨產業系 (113年起加入)",
      "y111": 0,
      "y112": 0,
      "y113": 5,
      "y114": 5,
      "y115": 7,
      "total": 17
    }
  ],
  "top15_enrolled_schools": [
    {
      "rank": 1,
      "school": "中山工商",
      "type": "高屏技高",
      "y111": 18,
      "y112": 21,
      "y113": 35,
      "y114": 11,
      "y115": 16,
      "total": 101,
      "note": "全校第 1 主力（近 2 年回升，為地利深耕重點）"
    },
    {
      "rank": 2,
      "school": "高雄小港高中",
      "type": "高屏普高",
      "y111": 11,
      "y112": 6,
      "y113": 5,
      "y114": 13,
      "y115": 9,
      "total": 44,
      "note": "普高第 1 主力（長年穩定就讀）"
    },
    {
      "rank": 3,
      "school": "樹德家商",
      "type": "高屏技高",
      "y111": 12,
      "y112": 7,
      "y113": 3,
      "y114": 9,
      "y115": 10,
      "total": 41,
      "note": "技高穩定來源（115 學年達 10 人）"
    },
    {
      "rank": 4,
      "school": "復華高中",
      "type": "高屏私高",
      "y111": 13,
      "y112": 7,
      "y113": 6,
      "y114": 9,
      "y115": 1,
      "total": 36,
      "note": "流失警訊（111-114 年均 6-13 人，115 年驟降至 1 人）"
    },
    {
      "rank": 5,
      "school": "立志高中",
      "type": "高屏私高",
      "y111": 7,
      "y112": 8,
      "y113": 8,
      "y114": 2,
      "y115": 10,
      "total": 35,
      "note": "綜合發展（兼具職科與普通科，115 年回升）"
    },
    {
      "rank": 6,
      "school": "潮州高中",
      "type": "高屏普高",
      "y111": 6,
      "y112": 7,
      "y113": 11,
      "y114": 5,
      "y115": 3,
      "total": 32,
      "note": "屏東核心普高來源（主要進入護理與物治）"
    },
    {
      "rank": 7,
      "school": "高雄林園高中",
      "type": "高屏普高",
      "y111": 4,
      "y112": 6,
      "y113": 5,
      "y114": 3,
      "y115": 12,
      "total": 30,
      "note": "快速成長型（115 學年大幅增長至 12 人）"
    },
    {
      "rank": 8,
      "school": "岡山高中",
      "type": "高屏普高",
      "y111": 4,
      "y112": 8,
      "y113": 5,
      "y114": 5,
      "y115": 4,
      "total": 26,
      "note": "北高雄穩定公立生源"
    },
    {
      "rank": 9,
      "school": "道明高中",
      "type": "高屏私高",
      "y111": 12,
      "y112": 4,
      "y113": 4,
      "y114": 2,
      "y115": 3,
      "total": 25,
      "note": "早期人數較多，近 4 年維持 2～4 人"
    },
    {
      "rank": 10,
      "school": "高雄文山高中",
      "type": "高屏普高",
      "y111": 8,
      "y112": 2,
      "y113": 4,
      "y114": 2,
      "y115": 7,
      "total": 23,
      "note": "社區公立高中，115 年回升至 7 人"
    },
    {
      "rank": 11,
      "school": "高雄左營高中",
      "type": "高屏普高",
      "y111": 6,
      "y112": 3,
      "y113": 3,
      "y114": 5,
      "y115": 4,
      "total": 21,
      "note": "穩定供給"
    },
    {
      "rank": 12,
      "school": "屏榮高中",
      "type": "高屏技高",
      "y111": 5,
      "y112": 4,
      "y113": 5,
      "y114": 2,
      "y115": 2,
      "total": 18,
      "note": "屏東主力私立職科生源"
    },
    {
      "rank": 13,
      "school": "巨人高中",
      "type": "中部私高",
      "y111": 0,
      "y112": 9,
      "y113": 5,
      "y114": 3,
      "y115": 1,
      "total": 18,
      "note": "雲林醫護專班重點學校（主要就讀甄選物治/護理）"
    },
    {
      "rank": 14,
      "school": "高雄鼓山高中",
      "type": "高屏普高",
      "y111": 4,
      "y112": 1,
      "y113": 3,
      "y114": 4,
      "y115": 5,
      "total": 17,
      "note": "社區公立高中穩定持平"
    },
    {
      "rank": 15,
      "school": "高雄仁武高中",
      "type": "高屏普高",
      "y111": 3,
      "y112": 1,
      "y113": 6,
      "y114": 3,
      "y115": 4,
      "total": 17,
      "note": "在地公立高中持平"
    },
    {
      "rank": 99,
      "school": "(個別報名/重考)",
      "type": "其他",
      "y111": 48,
      "y112": 7,
      "y113": 22,
      "y114": 13,
      "y115": 3,
      "total": 93,
      "note": "早期重考/非應屆較多，近年大幅降至 3 人"
    }
  ],
  "enrolled_regions": [
    {
      "region": "高屏地區",
      "cities": "高雄市、屏東縣",
      "y111": 182,
      "y112": 140,
      "y113": 163,
      "y114": 137,
      "y115": 156,
      "total": 778,
      "pct": "60.6%"
    },
    {
      "region": "南部地區",
      "cities": "臺南市、嘉義縣市",
      "y111": 66,
      "y112": 32,
      "y113": 20,
      "y114": 28,
      "y115": 27,
      "total": 173,
      "pct": "13.5%"
    },
    {
      "region": "中部地區",
      "cities": "中彰投、雲林、苗栗",
      "y111": 59,
      "y112": 31,
      "y113": 28,
      "y114": 23,
      "y115": 24,
      "total": 165,
      "pct": "12.9%"
    },
    {
      "region": "北部地區",
      "cities": "北北基、桃竹苗、宜蘭",
      "y111": 24,
      "y112": 20,
      "y113": 14,
      "y114": 11,
      "y115": 14,
      "total": 83,
      "pct": "6.5%"
    },
    {
      "region": "東部地區",
      "cities": "花蓮縣、臺東縣",
      "y111": 7,
      "y112": 7,
      "y113": 3,
      "y114": 5,
      "y115": 6,
      "total": 28,
      "pct": "2.2%"
    },
    {
      "region": "離島地區",
      "cities": "澎湖縣、金門縣、連江縣",
      "y111": 10,
      "y112": 6,
      "y113": 2,
      "y114": 4,
      "y115": 5,
      "total": 27,
      "pct": "2.1%"
    },
    {
      "region": "其他/未註記",
      "cities": "境外/同等學力等",
      "y111": 6,
      "y112": 5,
      "y113": 5,
      "y114": 13,
      "y115": 1,
      "total": 30,
      "pct": "2.3%"
    }
  ],
  "top15_applicant_schools": [
    {
      "rank": 1,
      "school": "中山工商",
      "type": "技高",
      "y111": 75,
      "y112": 81,
      "y113": 128,
      "y114": 54,
      "y115": 62,
      "total_apply": 400,
      "total_enrolled": 101,
      "conv_rate": "25.3%",
      "note": "高報名、高就讀（5 年報名 400 人次，就讀 101 人）"
    },
    {
      "rank": 2,
      "school": "道明高中",
      "type": "私立普高",
      "y111": 56,
      "y112": 37,
      "y113": 46,
      "y114": 26,
      "y115": 25,
      "total_apply": 190,
      "total_enrolled": 25,
      "conv_rate": "13.2%",
      "note": "高報名、低轉換（報名多但多跨校選填，就讀 25 人）"
    },
    {
      "rank": 3,
      "school": "高雄小港高中",
      "type": "公立普高",
      "y111": 33,
      "y112": 28,
      "y113": 24,
      "y114": 37,
      "y115": 31,
      "total_apply": 153,
      "total_enrolled": 44,
      "conv_rate": "28.8%",
      "note": "穩定首選，轉化就讀意願極高（就讀 44 人）"
    },
    {
      "rank": 4,
      "school": "高雄左營高中",
      "type": "公立普高",
      "y111": 24,
      "y112": 23,
      "y113": 27,
      "y114": 29,
      "y115": 32,
      "total_apply": 135,
      "total_enrolled": 21,
      "conv_rate": "15.6%",
      "note": "報名逐年上升，115 年達 32 人次"
    },
    {
      "rank": 5,
      "school": "潮州高中",
      "type": "公立普高",
      "y111": 23,
      "y112": 38,
      "y113": 22,
      "y114": 32,
      "y115": 20,
      "total_apply": 135,
      "total_enrolled": 32,
      "conv_rate": "23.7%",
      "note": "屏東代表性普高，意願穩定"
    },
    {
      "rank": 6,
      "school": "復華高中",
      "type": "私高",
      "y111": 44,
      "y112": 38,
      "y113": 20,
      "y114": 23,
      "y115": 10,
      "total_apply": 135,
      "total_enrolled": 36,
      "conv_rate": "26.7%",
      "note": "近年報名呈下滑趨勢（115 年僅 10 人次）"
    },
    {
      "rank": 7,
      "school": "巨人高中",
      "type": "醫護技高",
      "y111": 0,
      "y112": 40,
      "y113": 43,
      "y114": 33,
      "y115": 15,
      "total_apply": 131,
      "total_enrolled": 18,
      "conv_rate": "13.7%",
      "note": "中部衛護類專班重點報名校"
    },
    {
      "rank": 8,
      "school": "樹德家商",
      "type": "技高",
      "y111": 33,
      "y112": 32,
      "y113": 24,
      "y114": 13,
      "y115": 19,
      "total_apply": 121,
      "total_enrolled": 41,
      "conv_rate": "33.9%",
      "note": "技職美容、幼保主要來源"
    },
    {
      "rank": 9,
      "school": "國立溪湖高中",
      "type": "中部綜合/普高",
      "y111": 31,
      "y112": 27,
      "y113": 19,
      "y114": 19,
      "y115": 22,
      "total_apply": 118,
      "total_enrolled": 8,
      "conv_rate": "6.8%",
      "note": "中部跨區報名主力（多報考護理系）"
    },
    {
      "rank": 10,
      "school": "國立岡山高中",
      "type": "公立普高",
      "y111": 17,
      "y112": 33,
      "y113": 25,
      "y114": 18,
      "y115": 22,
      "total_apply": 115,
      "total_enrolled": 26,
      "conv_rate": "22.6%",
      "note": "北高雄穩定報名來源"
    },
    {
      "rank": 11,
      "school": "高雄林園高中",
      "type": "在地公立普高",
      "y111": 15,
      "y112": 20,
      "y113": 25,
      "y114": 14,
      "y115": 36,
      "total_apply": 110,
      "total_enrolled": 30,
      "conv_rate": "27.3%",
      "note": "暴衝型（115 學年報名暴增至 36 人次）"
    },
    {
      "rank": 12,
      "school": "立志高中",
      "type": "私高",
      "y111": 34,
      "y112": 20,
      "y113": 17,
      "y114": 21,
      "y115": 15,
      "total_apply": 107,
      "total_enrolled": 35,
      "conv_rate": "32.7%",
      "note": "雙軌報名（兼跨甄選與申請）"
    },
    {
      "rank": 13,
      "school": "國立屏東女中",
      "type": "公立明星普高",
      "y111": 18,
      "y112": 15,
      "y113": 18,
      "y114": 22,
      "y115": 23,
      "total_apply": 96,
      "total_enrolled": 13,
      "conv_rate": "13.5%",
      "note": "考量國北護/長庚科大備選志願多"
    },
    {
      "rank": 14,
      "school": "高雄中山高中",
      "type": "公立普高",
      "y111": 29,
      "y112": 15,
      "y113": 8,
      "y114": 16,
      "y115": 27,
      "total_apply": 95,
      "total_enrolled": 15,
      "conv_rate": "15.8%",
      "note": "楠梓區公立高中，115 年顯著回溫"
    },
    {
      "rank": 15,
      "school": "國立屏東高中",
      "type": "公立明星普高",
      "y111": 24,
      "y112": 21,
      "y113": 14,
      "y114": 15,
      "y115": 16,
      "total_apply": 90,
      "total_enrolled": 12,
      "conv_rate": "13.3%",
      "note": "物治與醫技相關志願居多"
    }
  ],
  "applicant_regions": [
    {
      "region": "高屏地區",
      "y111": 733,
      "y112": 731,
      "y113": 729,
      "y114": 662,
      "y115": 659,
      "total_apply": 3514,
      "apply_pct": "41.4%",
      "total_enrolled": 778,
      "conv_rate": "22.1%"
    },
    {
      "region": "中部地區",
      "y111": 414,
      "y112": 468,
      "y113": 368,
      "y114": 332,
      "y115": 289,
      "total_apply": 1871,
      "apply_pct": "22.0%",
      "total_enrolled": 165,
      "conv_rate": "8.8%"
    },
    {
      "region": "南部地區",
      "y111": 353,
      "y112": 265,
      "y113": 216,
      "y114": 210,
      "y115": 199,
      "total_apply": 1243,
      "apply_pct": "14.6%",
      "total_enrolled": 173,
      "conv_rate": "13.9%"
    },
    {
      "region": "北部地區",
      "y111": 283,
      "y112": 230,
      "y113": 163,
      "y114": 167,
      "y115": 194,
      "total_apply": 1037,
      "apply_pct": "12.2%",
      "total_enrolled": 83,
      "conv_rate": "8.0%"
    },
    {
      "region": "東部地區",
      "y111": 49,
      "y112": 38,
      "y113": 47,
      "y114": 53,
      "y115": 31,
      "total_apply": 218,
      "apply_pct": "2.6%",
      "total_enrolled": 28,
      "conv_rate": "12.8%"
    },
    {
      "region": "離島地區",
      "y111": 29,
      "y112": 35,
      "y113": 23,
      "y114": 14,
      "y115": 17,
      "total_apply": 118,
      "apply_pct": "1.4%",
      "total_enrolled": 27,
      "conv_rate": "22.9%"
    },
    {
      "region": "其他/未註記",
      "y111": 281,
      "y112": 46,
      "y113": 95,
      "y114": 44,
      "y115": 25,
      "total_apply": 491,
      "apply_pct": "5.8%",
      "total_enrolled": 30,
      "conv_rate": "—"
    }
  ],
  "cross_channel_geo": [
    {
      "region": "高屏地區",
      "zhenxuan_cnt": 339,
      "zhenxuan_pct": "64.3%",
      "shenqing_cnt": 451,
      "shenqing_pct": "59.6%",
      "note": "兩管道皆以高屏為底盤，甄選在地依賴度更高 (+4.7%)"
    },
    {
      "region": "南部地區 (南嘉)",
      "zhenxuan_cnt": 61,
      "zhenxuan_pct": "11.6%",
      "shenqing_cnt": 114,
      "shenqing_pct": "15.1%",
      "note": "普高南部跨區意願高（如台南二中、家齊、新化高中等）"
    },
    {
      "region": "中部地區 (中彰投雲)",
      "zhenxuan_cnt": 66,
      "zhenxuan_pct": "12.5%",
      "shenqing_cnt": 98,
      "shenqing_pct": "12.9%",
      "note": "甄選依賴衛護專校（巨人）；申請遍布各縣立/國立普高"
    },
    {
      "region": "北部地區",
      "zhenxuan_cnt": 31,
      "zhenxuan_pct": "5.9%",
      "shenqing_cnt": 52,
      "shenqing_pct": "6.9%",
      "note": "普高北部生因修讀護理專業意願較技高更為積極"
    },
    {
      "region": "東部地區",
      "zhenxuan_cnt": 8,
      "zhenxuan_pct": "1.5%",
      "shenqing_cnt": 20,
      "shenqing_pct": "2.6%",
      "note": "普高東部生源（花蓮女中、台東高中等）高出技高近一倍"
    },
    {
      "region": "離島地區",
      "zhenxuan_cnt": 10,
      "zhenxuan_pct": "1.9%",
      "shenqing_cnt": 17,
      "shenqing_pct": "2.2%",
      "note": "馬公高中、金門高中以申請管道為主力"
    },
    {
      "region": "其他",
      "zhenxuan_cnt": 12,
      "zhenxuan_pct": "2.3%",
      "shenqing_cnt": 5,
      "shenqing_pct": "0.7%",
      "note": "甄選管道個別報名重考生比重較高"
    }
  ]
};

        let currentStage = 'stage0';
        let currentYear = 'all';
        let currentChannel = 'all';
        let currentView = 'chart';

        // Chart instances dictionary
        const chartInstances = {};

        document.addEventListener('DOMContentLoaded', () => {
            initApp();
        });

        function initApp() {
            updateKpiCards();
            renderStage1Tables();
            renderStage2Tables();
            renderStage3Tables();
            initCharts();
        }

        // Global Option Filters
        function setYearFilter(year) {
            currentYear = year;
            updateOptionButtons('year', year);
            refreshAllViews();
        }

        function setChannelFilter(channel) {
            currentChannel = channel;
            updateOptionButtons('channel', channel);
            refreshAllViews();
        }

        function setViewMode(view) {
            currentView = view;
            updateOptionButtons('view', view);
            
            const chartBoxes = document.querySelectorAll('.card-chart-box');
            const tableBoxes = document.querySelectorAll('.card-table-box');

            if (view === 'chart') {
                chartBoxes.forEach(el => el.style.display = 'block');
                tableBoxes.forEach(el => el.style.display = 'none');
            } else if (view === 'table') {
                chartBoxes.forEach(el => el.style.display = 'none');
                tableBoxes.forEach(el => el.style.display = 'block');
            } else {
                chartBoxes.forEach(el => el.style.display = 'block');
                tableBoxes.forEach(el => el.style.display = 'block');
            }
        }

        function updateOptionButtons(group, val) {
            document.querySelectorAll(`[data-${group}]`).forEach(btn => {
                if (btn.getAttribute(`data-${group}`) === val) {
                    btn.classList.add('active');
                } else {
                    btn.classList.remove('active');
                }
            });
        }

        function switchStage(stageId) {
            currentStage = stageId;
            document.querySelectorAll('.stage-tab').forEach(tab => {
                if (tab.getAttribute('data-stage') === stageId) {
                    tab.classList.add('active');
                } else {
                    tab.classList.remove('active');
                }
            });

            document.querySelectorAll('.stage-content').forEach(sec => {
                sec.classList.remove('active');
            });

            const target = document.getElementById(stageId);
            if (target) target.classList.add('active');
        }

        function refreshAllViews() {
            updateKpiCards();
            renderStage1Tables();
            renderStage2Tables();
            renderStage3Tables();
            initCharts();
        }

        // DYNAMICALLY UPDATE TOP KPI STAT CARDS BASED ON SELECTED YEAR & CHANNEL
        function updateKpiCards() {
            const zf = DASHBOARD_DATA.zhenxuan_funnel;
            const sf = DASHBOARD_DATA.shenqing_funnel;
            const er = DASHBOARD_DATA.enrolled_regions;

            if (currentYear === 'all') {
                document.getElementById('kpiTitle1').innerText = '5年總一階通過人數';
                document.getElementById('kpiValue1').innerHTML = '8,492 <span style="font-size:16px">人次</span>';
                document.getElementById('kpiDesc1').innerText = '甄選 2,632 人次 ‧ 申請 5,860 人次';

                document.getElementById('kpiTitle2').innerText = '5年總正式報到人數';
                document.getElementById('kpiValue2').innerHTML = '1,284 <span style="font-size:16px">人</span>';
                document.getElementById('kpiDesc2').innerText = '甄選 527 人 ‧ 申請 757 人';

                document.getElementById('kpiTitle3').innerText = '申請入學就讀轉換率';
                document.getElementById('kpiValue3').innerText = '32.8%';
                document.getElementById('kpiDesc3').innerHTML = '二階報名 2,310人 ➔ 報到 757人';

                document.getElementById('kpiTitle4').innerText = '甄選入學分發報到率';
                document.getElementById('kpiValue4').innerText = '95.6%';
                document.getElementById('kpiDesc4').innerText = '分發即確定就讀 ‧ 高黏著強意願';

                document.getElementById('kpiTitle5').innerText = '高屏在地生源就讀比率';
                document.getElementById('kpiValue5').innerText = '60.6%';
                document.getElementById('kpiDesc5').innerText = '5年累計 778 人 ‧ 地利扎根核心';
            } else {
                // Single Year Filtered Stats
                const zItem = zf.find(x => x.year === currentYear) || {};
                const sItem = sf.find(x => x.year === currentYear) || {};
                const regKaohsiungPing = er.find(x => x.region === '高屏地區') || {};
                
                const zPass = zItem.p1_pass_cnt || 0;
                const sPass = sItem.p1_pass_cnt || 0;
                const totalPass = zPass + sPass;

                const zEnrolled = zItem.enrolled || 0;
                const sEnrolled = sItem.final_enrolled || 0;
                const totalEnrolled = zEnrolled + sEnrolled;

                const keyYear = 'y' + currentYear;
                const kpEnrolledYr = regKaohsiungPing[keyYear] || 0;
                const kpPctYr = totalEnrolled > 0 ? ((kpEnrolledYr / totalEnrolled) * 100).toFixed(1) + '%' : '0%';

                const sRateYr = sItem.p2_to_enrolled_rate || '—';
                const zRateYr = zItem.admitted_to_enrolled_rate !== '—' ? zItem.admitted_to_enrolled_rate : (zItem.p1_to_p2_rate + ' (報名率)');

                document.getElementById('kpiTitle1').innerText = `${currentYear}學年一階通過人數`;
                document.getElementById('kpiValue1').innerHTML = `${totalPass.toLocaleString()} <span style="font-size:16px">人次</span>`;
                document.getElementById('kpiDesc1').innerText = `甄選 ${zPass.toLocaleString()} 人次 ‧ 申請 ${sPass.toLocaleString()} 人次`;

                document.getElementById('kpiTitle2').innerText = `${currentYear}學年正式報到人數`;
                document.getElementById('kpiValue2').innerHTML = `${totalEnrolled} <span style="font-size:16px">人</span>`;
                document.getElementById('kpiDesc2').innerText = `甄選 ${zEnrolled} 人 ‧ 申請 ${sEnrolled} 人`;

                document.getElementById('kpiTitle3').innerText = `${currentYear}學年申請就讀轉換率`;
                document.getElementById('kpiValue3').innerText = sRateYr;
                document.getElementById('kpiDesc3').innerText = `二階報名 ${sItem.p2_apply_cnt || 0}人 ➔ 報到 ${sEnrolled}人`;

                document.getElementById('kpiTitle4').innerText = `${currentYear}學年甄選報到/報名率`;
                document.getElementById('kpiValue4').innerText = zRateYr;
                document.getElementById('kpiDesc4').innerText = `篩選通過 ${zPass}人次 ➔ 報到 ${zEnrolled}人`;

                document.getElementById('kpiTitle5').innerText = `${currentYear}學年高屏在地就讀比率`;
                document.getElementById('kpiValue5').innerText = kpPctYr;
                document.getElementById('kpiDesc5').innerText = `${currentYear}學年高屏地區報到 ${kpEnrolledYr} 人`;
            }
        }

        // Table Renderers with Filter & Highlight
        function renderStage1Tables() {
            const tbody = document.getElementById('tbodyStage1');
            tbody.innerHTML = '';

            const zf = DASHBOARD_DATA.zhenxuan_funnel;
            const sf = DASHBOARD_DATA.shenqing_funnel;

            zf.forEach(item => {
                if (currentYear !== 'all' && item.year !== currentYear) return;
                if (currentChannel === 'shenqing') return;
                const isHl = currentYear !== 'all' && item.year === currentYear;
                tbody.innerHTML += `
                    <tr class="${isHl ? 'row-highlight' : ''}">
                        <td><span class="badge-tag badge-quant">甄選 (技高)</span></td>
                        <td><b>${item.year}學年</b></td>
                        <td>${item.p1_pass_cnt} 人次 (${item.p1_pass_people}人)</td>
                        <td>${item.p2_apply_cnt ? item.p2_apply_cnt + ' 人次' : '(密碼保護)'}</td>
                        <td>${item.admitted ? item.admitted + ' 人' : '(密碼保護)'}</td>
                        <td><b style="color:#2563eb">${item.enrolled} 人</b></td>
                        <td>${item.p1_to_p2_rate}</td>
                        <td><span class="badge-highlight">${item.admitted_to_enrolled_rate}</span></td>
                    </tr>
                `;
            });

            sf.forEach(item => {
                if (currentYear !== 'all' && item.year !== currentYear) return;
                if (currentChannel === 'zhenxuan') return;
                const isHl = currentYear !== 'all' && item.year === currentYear;
                tbody.innerHTML += `
                    <tr class="${isHl ? 'row-highlight' : ''}">
                        <td><span class="badge-tag badge-strat">申請 (普高)</span></td>
                        <td><b>${item.year}學年</b></td>
                        <td>${item.p1_pass_cnt} 人次 (${item.p1_pass_people}人)</td>
                        <td>${item.p2_apply_cnt} 人次 (${item.p2_apply_people}人)</td>
                        <td>${item.confirmed} 人</td>
                        <td><b style="color:#059669">${item.final_enrolled} 人</b></td>
                        <td>—</td>
                        <td><span class="badge-highlight">${item.p2_to_enrolled_rate}</span></td>
                    </tr>
                `;
            });

            // Department tables
            const tbodyZ = document.getElementById('tbodyZhenxuanDepts');
            tbodyZ.innerHTML = '';
            DASHBOARD_DATA.zhenxuan_depts.forEach(d => {
                tbodyZ.innerHTML += `
                    <tr>
                        <td><b>${d.dept}</b></td>
                        <td style="${currentYear==='111'?'font-weight:bold;color:#2563eb':''}">${d.y111}</td>
                        <td style="${currentYear==='112'?'font-weight:bold;color:#2563eb':''}">${d.y112}</td>
                        <td style="${currentYear==='113'?'font-weight:bold;color:#2563eb':''}">${d.y113}</td>
                        <td style="${currentYear==='114'?'font-weight:bold;color:#2563eb':''}">${d.y114}</td>
                        <td style="${currentYear==='115'?'font-weight:bold;color:#2563eb':''}">${d.y115}</td>
                        <td><b style="color:#2563eb">${d.total}</b></td>
                    </tr>
                `;
            });

            const tbodyS = document.getElementById('tbodyShenqingDepts');
            tbodyS.innerHTML = '';
            DASHBOARD_DATA.shenqing_depts.forEach(d => {
                tbodyS.innerHTML += `
                    <tr>
                        <td><b>${d.dept}</b></td>
                        <td style="${currentYear==='111'?'font-weight:bold;color:#059669':''}">${d.y111}</td>
                        <td style="${currentYear==='112'?'font-weight:bold;color:#059669':''}">${d.y112}</td>
                        <td style="${currentYear==='113'?'font-weight:bold;color:#059669':''}">${d.y113}</td>
                        <td style="${currentYear==='114'?'font-weight:bold;color:#059669':''}">${d.y114}</td>
                        <td style="${currentYear==='115'?'font-weight:bold;color:#059669':''}">${d.y115}</td>
                        <td><b style="color:#059669">${d.total}</b></td>
                    </tr>
                `;
            });
        }

        function renderStage2Tables() {
            const tbodyTop = document.getElementById('tbodyTop15Full');
            tbodyTop.innerHTML = '';

            let schoolList = [...DASHBOARD_DATA.top15_applicant_schools];
            if (currentYear !== 'all') {
                const key = 'y' + currentYear;
                schoolList.sort((a, b) => {
                    const matchA = DASHBOARD_DATA.top15_enrolled_schools.find(e => e.school === a.school);
                    const matchB = DASHBOARD_DATA.top15_enrolled_schools.find(e => e.school === b.school);
                    const valA = matchA ? matchA[key] : 0;
                    const valB = matchB ? matchB[key] : 0;
                    return valB - valA;
                });
            }

            schoolList.forEach((s, idx) => {
                const enrolledMatch = DASHBOARD_DATA.top15_enrolled_schools.find(e => e.school === s.school);
                const enrolledY111 = enrolledMatch ? enrolledMatch.y111 : 0;
                const enrolledY112 = enrolledMatch ? enrolledMatch.y112 : 0;
                const enrolledY113 = enrolledMatch ? enrolledMatch.y113 : 0;
                const enrolledY114 = enrolledMatch ? enrolledMatch.y114 : 0;
                const enrolledY115 = enrolledMatch ? enrolledMatch.y115 : 0;
                
                let subTotal = s.total_enrolled;
                if (currentYear !== 'all') {
                    const key = 'y' + currentYear;
                    subTotal = enrolledMatch ? enrolledMatch[key] : 0;
                }

                tbodyTop.innerHTML += `
                    <tr>
                        <td><b>${currentYear === 'all' ? s.rank : idx + 1}</b></td>
                        <td><b>${s.school}</b></td>
                        <td>${s.type}</td>
                        <td style="${currentYear==='111'?'font-weight:bold;color:#2563eb':''}">${enrolledY111}</td>
                        <td style="${currentYear==='112'?'font-weight:bold;color:#2563eb':''}">${enrolledY112}</td>
                        <td style="${currentYear==='113'?'font-weight:bold;color:#2563eb':''}">${enrolledY113}</td>
                        <td style="${currentYear==='114'?'font-weight:bold;color:#2563eb':''}">${enrolledY114}</td>
                        <td style="${currentYear==='115'?'font-weight:bold;color:#2563eb':''}">${enrolledY115}</td>
                        <td><b style="color:#2563eb">${subTotal}</b></td>
                        <td>${s.total_apply}</td>
                        <td><span class="badge-highlight">${s.conv_rate}</span></td>
                        <td style="font-size:13px; color:var(--text-muted);">${s.note}</td>
                    </tr>
                `;
            });

            const tbodyReg = document.getElementById('tbodyRegionsFull');
            tbodyReg.innerHTML = '';
            DASHBOARD_DATA.applicant_regions.forEach(r => {
                const enrolledMatch = DASHBOARD_DATA.enrolled_regions.find(e => e.region === r.region);
                const enrolledTotal = enrolledMatch ? enrolledMatch.total : 0;
                const enrolledPct = enrolledMatch ? enrolledMatch.pct : '—';
                const y111 = enrolledMatch ? enrolledMatch.y111 : 0;
                const y112 = enrolledMatch ? enrolledMatch.y112 : 0;
                const y113 = enrolledMatch ? enrolledMatch.y113 : 0;
                const y114 = enrolledMatch ? enrolledMatch.y114 : 0;
                const y115 = enrolledMatch ? enrolledMatch.y115 : 0;
                const cities = enrolledMatch ? enrolledMatch.cities : '—';

                let subTotal = enrolledTotal;
                if (currentYear !== 'all') {
                    const key = 'y' + currentYear;
                    subTotal = enrolledMatch ? enrolledMatch[key] : 0;
                }

                tbodyReg.innerHTML += `
                    <tr>
                        <td><b>${r.region}</b></td>
                        <td style="font-size:13px;">${cities}</td>
                        <td>${r.total_apply}</td>
                        <td>${r.apply_pct}</td>
                        <td style="${currentYear==='111'?'font-weight:bold;color:#059669':''}">${y111}</td>
                        <td style="${currentYear==='112'?'font-weight:bold;color:#059669':''}">${y112}</td>
                        <td style="${currentYear==='113'?'font-weight:bold;color:#059669':''}">${y113}</td>
                        <td style="${currentYear==='114'?'font-weight:bold;color:#059669':''}">${y114}</td>
                        <td style="${currentYear==='115'?'font-weight:bold;color:#059669':''}">${y115}</td>
                        <td><b style="color:#059669">${subTotal}</b></td>
                        <td>${enrolledPct}</td>
                        <td><span class="badge-highlight">${r.conv_rate}</span></td>
                    </tr>
                `;
            });
        }

        function renderStage3Tables() {
            const tbodyCross = document.getElementById('tbodyCrossGeo');
            tbodyCross.innerHTML = '';
            DASHBOARD_DATA.cross_channel_geo.forEach(c => {
                tbodyCross.innerHTML += `
                    <tr>
                        <td><b>${c.region}</b></td>
                        <td>${c.zhenxuan_cnt} 人 (${c.zhenxuan_pct})</td>
                        <td>${c.shenqing_cnt} 人 (${c.shenqing_pct})</td>
                        <td style="font-size:14px; color:var(--text-muted);">${c.note}</td>
                    </tr>
                `;
            });
        }

        // Initialize & Dynamically Update Chart.js Graphs based on Filter State
        function initCharts() {
            createZhenxuanFunnelChart();
            createShenqingFunnelChart();
            createTop15EnrolledChart();
            createRegionTrendChart();
            createBCGMatrixChart();
        }

        function createZhenxuanFunnelChart() {
            const ctx = document.getElementById('chartZhenxuanFunnel');
            if (!ctx) return;
            if (chartInstances['chartZhenxuanFunnel']) chartInstances['chartZhenxuanFunnel'].destroy();

            const titleEl = document.getElementById('titleZhenxuanChart');

            if (currentYear === 'all') {
                if (titleEl) titleEl.innerHTML = '<i class="fa-solid fa-filter"></i> 四技甄選入學 (技高) 歷年各階段人數消長 (111~115學年)';
                const labels = ['111學年', '112學年', '113學年', '114學年', '115學年'];
                const dataP1 = [793, 531, 556, 399, 353];
                const dataP2 = [422, 230, 0, 162, 162];
                const dataEnrolled = [161, 93, 109, 86, 78];

                chartInstances['chartZhenxuanFunnel'] = new Chart(ctx, {
                    type: 'bar',
                    data: {
                        labels: labels,
                        datasets: [
                            { label: '一階篩選通過 (人次)', data: dataP1, backgroundColor: '#2563eb', borderRadius: 6 },
                            { label: '二階報名 (人數)', data: dataP2, backgroundColor: '#7c3aed', borderRadius: 6 },
                            { label: '實際已報到 (人數)', data: dataEnrolled, backgroundColor: '#059669', borderRadius: 6 }
                        ]
                    },
                    options: {
                        responsive: true,
                        maintainAspectRatio: false,
                        plugins: { legend: { labels: { color: '#334155', font: { size: 14, weight: 'bold' } } } },
                        scales: {
                            x: { ticks: { color: '#475569', font: { size: 13 } }, grid: { color: 'rgba(0,0,0,0.06)' } },
                            y: { ticks: { color: '#475569', font: { size: 13 } }, grid: { color: 'rgba(0,0,0,0.06)' } }
                        }
                    }
                });
            } else {
                if (titleEl) titleEl.innerHTML = `<i class="fa-solid fa-filter"></i> 四技甄選入學 (技高) - ${currentYear}學年階段漏斗歷程`;
                const zItem = DASHBOARD_DATA.zhenxuan_funnel.find(x => x.year === currentYear) || {};
                const labels = ['一階篩選通過', '二階報名複試', '志願分發/最終報到'];
                const funnelData = [
                    zItem.p1_pass_cnt || 0,
                    zItem.p2_apply_cnt || 0,
                    zItem.enrolled || 0
                ];

                chartInstances['chartZhenxuanFunnel'] = new Chart(ctx, {
                    type: 'bar',
                    data: {
                        labels: labels,
                        datasets: [{
                            label: `${currentYear}學年階段人數 (人)`,
                            data: funnelData,
                            backgroundColor: ['#2563eb', '#7c3aed', '#059669'],
                            borderRadius: 8
                        }]
                    },
                    options: {
                        indexAxis: 'y',
                        responsive: true,
                        maintainAspectRatio: false,
                        plugins: { legend: { labels: { color: '#334155', font: { size: 14, weight: 'bold' } } } },
                        scales: {
                            x: { ticks: { color: '#475569', font: { size: 13 } }, grid: { color: 'rgba(0,0,0,0.06)' } },
                            y: { ticks: { color: '#0f172a', font: { size: 14, weight: 'bold' } }, grid: { color: 'rgba(0,0,0,0.06)' } }
                        }
                    }
                });
            }
        }

        function createShenqingFunnelChart() {
            const ctx = document.getElementById('chartShenqingFunnel');
            if (!ctx) return;
            if (chartInstances['chartShenqingFunnel']) chartInstances['chartShenqingFunnel'].destroy();

            const titleEl = document.getElementById('titleShenqingChart');

            if (currentYear === 'all') {
                if (titleEl) titleEl.innerHTML = '<i class="fa-solid fa-filter"></i> 四技申請入學 (普高) 歷年各階段人數消長 (111~115學年)';
                const labels = ['111學年', '112學年', '113學年', '114學年', '115學年'];
                const dataP1 = [1349, 1282, 1085, 1083, 1061];
                const dataP2 = [656, 505, 382, 395, 372];
                const dataEnrolled = [193, 148, 126, 135, 155];

                chartInstances['chartShenqingFunnel'] = new Chart(ctx, {
                    type: 'bar',
                    data: {
                        labels: labels,
                        datasets: [
                            { label: '一階篩選通過 (人次)', data: dataP1, backgroundColor: '#0284c7', borderRadius: 6 },
                            { label: '二階報名 (人數)', data: dataP2, backgroundColor: '#9333ea', borderRadius: 6 },
                            { label: '最終已報到 (人數)', data: dataEnrolled, backgroundColor: '#10b981', borderRadius: 6 }
                        ]
                    },
                    options: {
                        responsive: true,
                        maintainAspectRatio: false,
                        plugins: { legend: { labels: { color: '#334155', font: { size: 14, weight: 'bold' } } } },
                        scales: {
                            x: { ticks: { color: '#475569', font: { size: 13 } }, grid: { color: 'rgba(0,0,0,0.06)' } },
                            y: { ticks: { color: '#475569', font: { size: 13 } }, grid: { color: 'rgba(0,0,0,0.06)' } }
                        }
                    }
                });
            } else {
                if (titleEl) titleEl.innerHTML = `<i class="fa-solid fa-filter"></i> 四技申請入學 (普高) - ${currentYear}學年階段漏斗歷程`;
                const sItem = DASHBOARD_DATA.shenqing_funnel.find(x => x.year === currentYear) || {};
                const labels = ['一階篩選通過', '二階報名複試', '報到確認/最終就讀'];
                const funnelData = [
                    sItem.p1_pass_cnt || 0,
                    sItem.p2_apply_cnt || 0,
                    sItem.final_enrolled || 0
                ];

                chartInstances['chartShenqingFunnel'] = new Chart(ctx, {
                    type: 'bar',
                    data: {
                        labels: labels,
                        datasets: [{
                            label: `${currentYear}學年階段人數 (人)`,
                            data: funnelData,
                            backgroundColor: ['#0284c7', '#9333ea', '#10b981'],
                            borderRadius: 8
                        }]
                    },
                    options: {
                        indexAxis: 'y',
                        responsive: true,
                        maintainAspectRatio: false,
                        plugins: { legend: { labels: { color: '#334155', font: { size: 14, weight: 'bold' } } } },
                        scales: {
                            x: { ticks: { color: '#475569', font: { size: 13 } }, grid: { color: 'rgba(0,0,0,0.06)' } },
                            y: { ticks: { color: '#0f172a', font: { size: 14, weight: 'bold' } }, grid: { color: 'rgba(0,0,0,0.06)' } }
                        }
                    }
                });
            }
        }

        function createTop15EnrolledChart() {
            const ctx = document.getElementById('chartTop15Enrolled');
            if (!ctx) return;
            if (chartInstances['chartTop15Enrolled']) chartInstances['chartTop15Enrolled'].destroy();

            const titleEl = document.getElementById('titleTop15Chart');

            let schools = [...DASHBOARD_DATA.top15_enrolled_schools];
            let labels = [];
            let totals = [];

            if (currentYear === 'all') {
                if (titleEl) titleEl.innerHTML = '<i class="fa-solid fa-school"></i> 近 5 年全校主要生源學校就讀總人數 (Top 15)';
                schools = schools.slice(0, 15);
                labels = schools.map(s => s.school);
                totals = schools.map(s => s.total);
            } else {
                if (titleEl) titleEl.innerHTML = `<i class="fa-solid fa-school"></i> ${currentYear}學年全校生源學校就讀人數排名 (Top 15)`;
                const key = 'y' + currentYear;
                schools.sort((a, b) => b[key] - a[key]);
                schools = schools.slice(0, 15);
                labels = schools.map(s => s.school);
                totals = schools.map(s => s[key]);
            }

            chartInstances['chartTop15Enrolled'] = new Chart(ctx, {
                type: 'bar',
                data: {
                    labels: labels,
                    datasets: [{
                        label: currentYear === 'all' ? '5年累計就讀人數' : `${currentYear}學年就讀人數`,
                        data: totals,
                        backgroundColor: '#2563eb',
                        borderColor: '#1d4ed8',
                        borderWidth: 1,
                        borderRadius: 6
                    }]
                },
                options: {
                    indexAxis: 'y',
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                        legend: { labels: { color: '#334155', font: { size: 14, weight: 'bold' } } }
                    },
                    scales: {
                        x: { ticks: { color: '#475569', font: { size: 13 } }, grid: { color: 'rgba(0,0,0,0.06)' } },
                        y: { ticks: { color: '#0f172a', font: { size: 13, weight: 'bold' } }, grid: { color: 'rgba(0,0,0,0.06)' } }
                    }
                }
            });
        }

        function createRegionTrendChart() {
            const ctx = document.getElementById('chartRegionTrend');
            if (!ctx) return;
            if (chartInstances['chartRegionTrend']) chartInstances['chartRegionTrend'].destroy();

            const titleEl = document.getElementById('titleRegionChart');

            if (currentYear === 'all') {
                if (titleEl) titleEl.innerHTML = '<i class="fa-solid fa-map-location-dot"></i> 近 5 年就讀學生之「生源區域」分佈與變化';
                const labels = ['111學年', '112學年', '113學年', '114學年', '115學年'];
                const datasets = [
                    { label: '高屏地區', data: [182, 140, 163, 137, 156], borderColor: '#2563eb', backgroundColor: '#2563eb', tension: 0.3, borderWidth: 3 },
                    { label: '南部地區', data: [66, 32, 20, 28, 27], borderColor: '#059669', backgroundColor: '#059669', tension: 0.3, borderWidth: 3 },
                    { label: '中部地區', data: [59, 31, 28, 23, 24], borderColor: '#7c3aed', backgroundColor: '#7c3aed', tension: 0.3, borderWidth: 3 },
                    { label: '北部地區', data: [24, 20, 14, 11, 14], borderColor: '#d97706', backgroundColor: '#d97706', tension: 0.3, borderWidth: 3 }
                ];

                chartInstances['chartRegionTrend'] = new Chart(ctx, {
                    type: 'line',
                    data: { labels: labels, datasets: datasets },
                    options: {
                        responsive: true,
                        maintainAspectRatio: false,
                        plugins: { legend: { labels: { color: '#334155', font: { size: 14, weight: 'bold' } } } },
                        scales: {
                            x: { ticks: { color: '#475569', font: { size: 13 } }, grid: { color: 'rgba(0,0,0,0.06)' } },
                            y: { ticks: { color: '#475569', font: { size: 13 } }, grid: { color: 'rgba(0,0,0,0.06)' } }
                        }
                    }
                });
            } else {
                if (titleEl) titleEl.innerHTML = `<i class="fa-solid fa-map-location-dot"></i> ${currentYear}學年生源地理區域分佈 (Pie Chart)`;
                const key = 'y' + currentYear;
                const labels = DASHBOARD_DATA.enrolled_regions.map(r => r.region);
                const values = DASHBOARD_DATA.enrolled_regions.map(r => r[key]);

                chartInstances['chartRegionTrend'] = new Chart(ctx, {
                    type: 'doughnut',
                    data: {
                        labels: labels,
                        datasets: [{
                            label: `${currentYear}學年就讀人數`,
                            data: values,
                            backgroundColor: ['#2563eb', '#059669', '#7c3aed', '#d97706', '#0284c7', '#e11d48', '#64748b']
                        }]
                    },
                    options: {
                        responsive: true,
                        maintainAspectRatio: false,
                        plugins: {
                            legend: { position: 'right', labels: { color: '#334155', font: { size: 14, weight: 'bold' } } }
                        }
                    }
                });
            }
        }

        function createBCGMatrixChart() {
            const ctx = document.getElementById('chartBCGMatrix');
            if (!ctx) return;
            if (chartInstances['chartBCGMatrix']) chartInstances['chartBCGMatrix'].destroy();

            const titleEl = document.getElementById('titleBCGChart');

            let points = [];
            if (currentYear === 'all') {
                if (titleEl) titleEl.innerHTML = '<i class="fa-solid fa-chart-gantt"></i> 生源學校 BCG 矩陣 (5年報名總規模 vs 就讀轉換率 %)';
                points = DASHBOARD_DATA.top15_applicant_schools.map(s => ({
                    x: s.total_apply,
                    y: parseFloat(s.conv_rate.replace('%', '')),
                    school: s.school
                }));
            } else {
                if (titleEl) titleEl.innerHTML = `<i class="fa-solid fa-chart-gantt"></i> 生源學校 BCG 矩陣 (${currentYear}學年報名 vs 就讀人次散佈)`;
                const key = 'y' + currentYear;
                points = DASHBOARD_DATA.top15_applicant_schools.map(s => {
                    const match = DASHBOARD_DATA.top15_enrolled_schools.find(e => e.school === s.school);
                    const enrolledCount = match ? match[key] : 0;
                    const applyCount = s[key];
                    const rate = applyCount > 0 ? ((enrolledCount / applyCount) * 100).toFixed(1) : 0;
                    return {
                        x: applyCount,
                        y: parseFloat(rate),
                        school: s.school
                    };
                });
            }

            chartInstances['chartBCGMatrix'] = new Chart(ctx, {
                type: 'scatter',
                data: {
                    datasets: [{
                        label: '生源學校 (報名人次 vs 就讀轉換率%)',
                        data: points,
                        backgroundColor: '#e11d48',
                        pointRadius: 9,
                        pointHoverRadius: 14
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                        tooltip: {
                            callbacks: {
                                label: (ctx) => `${ctx.raw.school}: 報名 ${ctx.raw.x} 人次, 轉換率 ${ctx.raw.y}%`
                            }
                        },
                        legend: { labels: { color: '#334155', font: { size: 14, weight: 'bold' } } }
                    },
                    scales: {
                        x: { title: { display: true, text: '報名總人次', color: '#334155', font: { size: 14, weight: 'bold' } }, ticks: { color: '#475569', font: { size: 13 } }, grid: { color: 'rgba(0,0,0,0.06)' } },
                        y: { title: { display: true, text: '就讀轉換率 (%)', color: '#334155', font: { size: 14, weight: 'bold' } }, ticks: { color: '#475569', font: { size: 13 } }, grid: { color: 'rgba(0,0,0,0.06)' } }
                    }
                }
            });
        }

        // Export Chart Image (PNG)
        function exportChartImage(chartId, title) {
            const chart = chartInstances[chartId];
            if (!chart) return;
            const a = document.createElement('a');
            a.href = chart.toBase64Image();
            a.download = `${title}_${currentYear}_${new Date().toISOString().slice(0,10)}.png`;
            a.click();
        }

        // Export Table CSV
        function exportTableCSVFromElement(tableId, filename) {
            const table = document.getElementById(tableId);
            if (!table) return;
            let csv = [];
            for (let row of table.rows) {
                let cols = [];
                for (let cell of row.cells) {
                    cols.push('"' + cell.innerText.replace(/"/g, '""').trim() + '"');
                }
                csv.push(cols.join(','));
            }
            downloadCSV(csv.join(String.fromCharCode(10)), filename);
        }

        function exportTableCSVFromData(key, filename) {
            const rows = DASHBOARD_DATA[key];
            if (!rows || rows.length === 0) return;
            let keys = Object.keys(rows[0]);
            let csv = [keys.join(',')];
            rows.forEach(r => {
                let vals = keys.map(k => '"' + (r[k] !== null ? r[k] : '') + '"');
                csv.push(vals.join(','));
            });
            downloadCSV(csv.join(String.fromCharCode(10)), filename);
        }

        function exportAllTablesCSV() {
            exportTableCSVFromData('top15_applicant_schools', '全校Top15生源學校數據.csv');
        }

        function downloadCSV(csvContent, filename) {
            const blob = new Blob(['\uFEFF' + csvContent], { type: 'text/csv;charset=utf-8;' });
            const link = document.createElement('a');
            link.href = URL.createObjectURL(blob);
            link.download = filename;
            link.click();
        }

    </script>
</body>
</html>
'''

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html_content)

with open('生源變化分析戰情看板.html', 'w', encoding='utf-8') as f:
    f.write(html_content)

print('Done!')
