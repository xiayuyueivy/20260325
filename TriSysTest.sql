-- TriSysTest 測試資料建立腳本
-- Database: gemio12 (開發區: 163.17.141.61,8090)
-- Date: 2026-03-25

USE gemio12;
GO

-- ===========================
-- 建立資料表
-- ===========================

-- 1. CUST 客戶資料
IF OBJECT_ID('cust', 'U') IS NOT NULL DROP TABLE cust;
CREATE TABLE cust (
    cust_code VARCHAR(20) NOT NULL PRIMARY KEY,
    cust_name NVARCHAR(100),
    remark    NVARCHAR(200)
);

-- 2. FACT 廠商資料
IF OBJECT_ID('fact', 'U') IS NOT NULL DROP TABLE fact;
CREATE TABLE fact (
    fact_code VARCHAR(20) NOT NULL PRIMARY KEY,
    fact_name NVARCHAR(100),
    remark    NVARCHAR(200)
);

-- 3. ITEM 商品資料
IF OBJECT_ID('item', 'U') IS NOT NULL DROP TABLE item;
CREATE TABLE item (
    item_code VARCHAR(20) NOT NULL PRIMARY KEY,
    item_name NVARCHAR(100),
    fact_code VARCHAR(20)
);

-- 4. USER 用戶資料
IF OBJECT_ID('[user]', 'U') IS NOT NULL DROP TABLE [user];
CREATE TABLE [user] (
    userid   VARCHAR(20) NOT NULL PRIMARY KEY,
    username NVARCHAR(100),
    pwd      VARCHAR(50)
);

GO

-- ===========================
-- CUST 客戶 50 筆
-- ===========================
INSERT INTO cust (cust_code, cust_name, remark) VALUES
('CUST001', N'台灣科技股份有限公司',   N'北區重要客戶'),
('CUST002', N'勝利電子有限公司',       N'中區客戶'),
('CUST003', N'永豐商貿股份有限公司',   N'南區客戶'),
('CUST004', N'宏達資訊有限公司',       N'長期合作夥伴'),
('CUST005', N'聯發工業股份有限公司',   N'北區製造業'),
('CUST006', N'中華貿易股份有限公司',   N'進出口商'),
('CUST007', N'大同電器有限公司',       N'家電零售'),
('CUST008', N'東方精密機械公司',       N'機械設備商'),
('CUST009', N'新光紡織股份有限公司',   N'紡織業客戶'),
('CUST010', N'全球物流有限公司',       N'物流配送業'),
('CUST011', N'瑞興化工股份有限公司',   N'化工原料'),
('CUST012', N'金順食品有限公司',       N'食品飲料業'),
('CUST013', N'台翔航空服務公司',       N'航空周邊'),
('CUST014', N'建宏營造股份有限公司',   N'建築工程'),
('CUST015', N'華城電力有限公司',       N'電力設備'),
('CUST016', N'美德醫療器材公司',       N'醫療器材'),
('CUST017', N'正達汽車零件有限公司',   N'汽車零配件'),
('CUST018', N'明基電通股份有限公司',   N'消費電子'),
('CUST019', N'豐盛農業有限公司',       N'農業相關'),
('CUST020', N'華南紙業股份有限公司',   N'紙製品'),
('CUST021', N'智勝資訊科技公司',       N'IT 服務'),
('CUST022', N'光仁教育機構',           N'教育訓練'),
('CUST023', N'威盛環保工程公司',       N'環保工程'),
('CUST024', N'寶成工業股份有限公司',   N'製造業'),
('CUST025', N'亞太電信有限公司',       N'電信業'),
('CUST026', N'泰山食品股份有限公司',   N'食品加工'),
('CUST027', N'漢威安全系統公司',       N'安全監控'),
('CUST028', N'成功機電有限公司',       N'機電設備'),
('CUST029', N'麗寶樂園開發公司',       N'休閒娛樂'),
('CUST030', N'永記造漆工業公司',       N'塗料製造'),
('CUST031', N'台塑化工股份有限公司',   N'石化業'),
('CUST032', N'裕隆汽車有限公司',       N'汽車製造'),
('CUST033', N'嘉里物流公司',           N'倉儲物流'),
('CUST034', N'先進光電股份有限公司',   N'光電業'),
('CUST035', N'瑞昱半導體公司',         N'半導體'),
('CUST036', N'義聯集團有限公司',       N'鋼鐵業'),
('CUST037', N'昇恆昌免稅商店',         N'零售業'),
('CUST038', N'遠傳電信股份有限公司',   N'電信服務'),
('CUST039', N'富邦金融控股公司',       N'金融業'),
('CUST040', N'長榮海運股份有限公司',   N'海運業'),
('CUST041', N'奇美電子有限公司',       N'面板製造'),
('CUST042', N'和碩聯合科技公司',       N'電子代工'),
('CUST043', N'廣達電腦股份有限公司',   N'電腦製造'),
('CUST044', N'威剛科技有限公司',       N'記憶體模組'),
('CUST045', N'英業達股份有限公司',     N'伺服器製造'),
('CUST046', N'緯創資通有限公司',       N'電子製造'),
('CUST047', N'仁寶電腦工業公司',       N'筆電代工'),
('CUST048', N'鴻準精密工業公司',       N'精密零件'),
('CUST049', N'台達電子工業公司',       N'電源供應器'),
('CUST050', N'研華科技股份有限公司',   N'工業電腦');

GO

-- ===========================
-- FACT 廠商 50 筆
-- ===========================
INSERT INTO fact (fact_code, fact_name, remark) VALUES
('FACT001', N'新達原料供應公司',       N'原物料供應商'),
('FACT002', N'精誠電子元件公司',       N'電子零件'),
('FACT003', N'全球包材有限公司',       N'包裝材料'),
('FACT004', N'東昇螺絲工廠',           N'五金零件'),
('FACT005', N'豐田機械零件公司',       N'機械零件'),
('FACT006', N'勤益化學原料行',         N'化學原料'),
('FACT007', N'聖龍塑膠工業公司',       N'塑膠原料'),
('FACT008', N'大順布料有限公司',       N'紡織材料'),
('FACT009', N'旺福食品原料公司',       N'食品原料'),
('FACT010', N'安泰鋼材供應商',         N'鋼鐵材料'),
('FACT011', N'順發電線電纜公司',       N'電線電纜'),
('FACT012', N'美達光學元件公司',       N'光學零件'),
('FACT013', N'裕達橡膠製品公司',       N'橡膠零件'),
('FACT014', N'宏億木業有限公司',       N'木材供應'),
('FACT015', N'長春化工原料公司',       N'化工品'),
('FACT016', N'永昌紙業原料公司',       N'紙類原料'),
('FACT017', N'興中玻璃有限公司',       N'玻璃材料'),
('FACT018', N'台聯陶瓷原料公司',       N'陶瓷材料'),
('FACT019', N'明達皮革有限公司',       N'皮革原料'),
('FACT020', N'祥和印刷耗材公司',       N'印刷耗材'),
('FACT021', N'德豐金屬有限公司',       N'金屬材料'),
('FACT022', N'建源防水材料公司',       N'建材供應'),
('FACT023', N'榮成油墨有限公司',       N'油墨材料'),
('FACT024', N'啟翔電池供應商',         N'電池元件'),
('FACT025', N'合眾密封件公司',         N'密封零件'),
('FACT026', N'太平洋輸送帶公司',       N'輸送設備'),
('FACT027', N'新宇模具製作廠',         N'模具製造'),
('FACT028', N'聯泰鑄造有限公司',       N'鑄造零件'),
('FACT029', N'廣和噴霧設備公司',       N'噴霧設備'),
('FACT030', N'勝源濾材有限公司',       N'濾材供應'),
('FACT031', N'正豐軸承供應商',         N'軸承零件'),
('FACT032', N'三達馬達製造公司',       N'馬達供應'),
('FACT033', N'耀華氣動元件公司',       N'氣動零件'),
('FACT034', N'海燕電容器公司',         N'電容元件'),
('FACT035', N'金龍電阻製造廠',         N'電阻元件'),
('FACT036', N'博安繼電器公司',         N'繼電器'),
('FACT037', N'富源變壓器有限公司',     N'變壓器供應'),
('FACT038', N'朝陽感測器公司',         N'感測元件'),
('FACT039', N'亮點 LED 供應商',        N'LED 元件'),
('FACT040', N'碩聯連接器公司',         N'連接器零件'),
('FACT041', N'志誠散熱器公司',         N'散熱元件'),
('FACT042', N'銘傳風扇製造廠',         N'散熱風扇'),
('FACT043', N'采盈電源模組公司',       N'電源模組'),
('FACT044', N'廣利顯示器材料商',       N'顯示材料'),
('FACT045', N'昌盛磁鐵有限公司',       N'磁性零件'),
('FACT046', N'大慶彈簧工廠',           N'彈簧零件'),
('FACT047', N'天成閥門供應公司',       N'閥門設備'),
('FACT048', N'捷成泵浦有限公司',       N'泵浦設備'),
('FACT049', N'東升齒輪製造廠',         N'齒輪零件'),
('FACT050', N'聯宇鏈條有限公司',       N'鏈條傳動');

GO

-- ===========================
-- ITEM 商品 50 筆（fact_code 循環引用 FACT001~FACT010）
-- ===========================
INSERT INTO item (item_code, item_name, fact_code) VALUES
('ITEM001', N'不銹鋼螺絲組',         'FACT004'),
('ITEM002', N'高壓電容器 100uF',     'FACT034'),
('ITEM003', N'矽利康密封劑',         'FACT025'),
('ITEM004', N'PVC 電線 1.5mm',       'FACT011'),
('ITEM005', N'鋰電池組 18650',       'FACT024'),
('ITEM006', N'橡膠 O 型環',          'FACT013'),
('ITEM007', N'精密軸承 6205',        'FACT031'),
('ITEM008', N'無刷馬達 24V',         'FACT032'),
('ITEM009', N'氣動快速接頭',         'FACT033'),
('ITEM010', N'金屬板 304 不鏽鋼',    'FACT021'),
('ITEM011', N'LED 燈條 5050',        'FACT039'),
('ITEM012', N'繼電器 12V 10A',       'FACT036'),
('ITEM013', N'散熱鋁片 80x80',       'FACT041'),
('ITEM014', N'連接器 JST 2.54mm',    'FACT040'),
('ITEM015', N'電阻 10KΩ 1/4W',       'FACT035'),
('ITEM016', N'感測器溫度 NTC 10K',   'FACT038'),
('ITEM017', N'變壓器 220V/12V 5A',   'FACT037'),
('ITEM018', N'電源模組 DC-DC 5V3A',  'FACT043'),
('ITEM019', N'散熱風扇 12V 80mm',    'FACT042'),
('ITEM020', N'齒輪減速箱 1:20',      'FACT049'),
('ITEM021', N'彈簧壓縮彈簧 Φ5',     'FACT046'),
('ITEM022', N'閥門電磁閥 24V',       'FACT047'),
('ITEM023', N'微型泵浦 12V',         'FACT048'),
('ITEM024', N'鏈條 #40 滾子鏈',      'FACT050'),
('ITEM025', N'磁鐵圓形 Φ10×3mm',    'FACT045'),
('ITEM026', N'塑膠外殼 ABS 黑色',    'FACT007'),
('ITEM027', N'化學溶劑異丙醇',       'FACT006'),
('ITEM028', N'包裝紙箱 A3',          'FACT003'),
('ITEM029', N'玻璃纖維布',           'FACT017'),
('ITEM030', N'皮革人造皮 PU',        'FACT019'),
('ITEM031', N'電子元件套件組',       'FACT002'),
('ITEM032', N'鋁合金型材 6061',      'FACT021'),
('ITEM033', N'銅線 0.3mm 捲',        'FACT011'),
('ITEM034', N'輸送帶 PVC 500mm',     'FACT026'),
('ITEM035', N'模具鋼 P20',           'FACT027'),
('ITEM036', N'鑄鐵件 HT250',         'FACT028'),
('ITEM037', N'濾網 HEPA 級',         'FACT030'),
('ITEM038', N'光學鏡片 BK7',         'FACT012'),
('ITEM039', N'油墨黑色水性',         'FACT023'),
('ITEM040', N'防水矽膠條 8mm',       'FACT022'),
('ITEM041', N'木材松木板 18mm',      'FACT014'),
('ITEM042', N'陶瓷基板 Al2O3',       'FACT018'),
('ITEM043', N'食品級矽膠管',         'FACT013'),
('ITEM044', N'印刷耗材碳粉匣',       'FACT020'),
('ITEM045', N'鋼材角鐵 50×50×5',    'FACT010'),
('ITEM046', N'紙張 A4 80g 500入',    'FACT016'),
('ITEM047', N'原物料食品澱粉',       'FACT009'),
('ITEM048', N'布料棉質胚布',         'FACT008'),
('ITEM049', N'噴霧瓶 500mL',         'FACT029'),
('ITEM050', N'光學感測器 GP2Y0A21', 'FACT038');

GO

-- ===========================
-- USER 用戶 50 筆
-- ===========================
INSERT INTO [user] (userid, username, pwd) VALUES
('U001', N'admin',       'Admin@2026'),
('U002', N'john.chen',   'Pass1234'),
('U003', N'mary.wang',   'Pass1234'),
('U004', N'peter.liu',   'Pass1234'),
('U005', N'alice.chang', 'Pass1234'),
('U006', N'bob.lin',     'Pass1234'),
('U007', N'carol.wu',    'Pass1234'),
('U008', N'david.huang', 'Pass1234'),
('U009', N'emma.yang',   'Pass1234'),
('U010', N'frank.cheng', 'Pass1234'),
('U011', N'grace.tsai',  'Pass1234'),
('U012', N'henry.hsu',   'Pass1234'),
('U013', N'iris.chou',   'Pass1234'),
('U014', N'jack.lu',     'Pass1234'),
('U015', N'kate.chen',   'Pass1234'),
('U016', N'leo.wang',    'Pass1234'),
('U017', N'mia.liu',     'Pass1234'),
('U018', N'nick.chang',  'Pass1234'),
('U019', N'olivia.lin',  'Pass1234'),
('U020', N'paul.wu',     'Pass1234'),
('U021', N'queen.huang', 'Pass1234'),
('U022', N'ray.yang',    'Pass1234'),
('U023', N'sara.cheng',  'Pass1234'),
('U024', N'tom.tsai',    'Pass1234'),
('U025', N'una.hsu',     'Pass1234'),
('U026', N'victor.chou', 'Pass1234'),
('U027', N'wendy.lu',    'Pass1234'),
('U028', N'xander.chen', 'Pass1234'),
('U029', N'yuki.wang',   'Pass1234'),
('U030', N'zack.liu',    'Pass1234'),
('U031', N'ann.chang',   'Pass1234'),
('U032', N'ben.lin',     'Pass1234'),
('U033', N'cindy.wu',    'Pass1234'),
('U034', N'dan.huang',   'Pass1234'),
('U035', N'eva.yang',    'Pass1234'),
('U036', N'felix.cheng', 'Pass1234'),
('U037', N'gina.tsai',   'Pass1234'),
('U038', N'hugo.hsu',    'Pass1234'),
('U039', N'ida.chou',    'Pass1234'),
('U040', N'jason.lu',    'Pass1234'),
('U041', N'kelly.chen',  'Pass1234'),
('U042', N'liam.wang',   'Pass1234'),
('U043', N'mona.liu',    'Pass1234'),
('U044', N'ned.chang',   'Pass1234'),
('U045', N'ora.lin',     'Pass1234'),
('U046', N'pat.wu',      'Pass1234'),
('U047', N'quinn.huang', 'Pass1234'),
('U048', N'rose.yang',   'Pass1234'),
('U049', N'sam.cheng',   'Pass1234'),
('U050', N'tina.tsai',   'Pass1234');

GO

-- ===========================
-- 驗證筆數
-- ===========================
SELECT 'cust' AS tbl, COUNT(*) AS cnt FROM cust
UNION ALL
SELECT 'fact', COUNT(*) FROM fact
UNION ALL
SELECT 'item', COUNT(*) FROM item
UNION ALL
SELECT 'user', COUNT(*) FROM [user];
