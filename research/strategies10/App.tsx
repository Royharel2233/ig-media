import React from 'react';
import { Callout, Closing, Facts, FileCard, Group, Header, Paragraph, Photos, Route, Routes, Text, TextLink } from '@instinct/files';
import './style.css';
import hero from './photos/hero.png';

type Strategy = {
  n: number;
  name: string;
  what: string;
  facts: { label: string; value: string }[];
  verdict: string;
  source: { label: string; href: string };
};

const strategies: Strategy[] = [
  {
    n: 1,
    name: 'ארביטראז׳ בין-בורסתי',
    what: 'קנייה בבורסה זולה ומכירה בו-זמנית בבורסה יקרה על אותו נכס.',
    facts: [
      { label: 'ראיות', value: 'Makarov & Schoar, Journal of Financial Economics 2020' },
      { label: 'שכבת ראיות', value: 'תועד על דאטא שוק אמיתי (לא בקטסט בלבד)' },
      { label: 'עלויות', value: 'עמלות, העברות בין בורסות, החזקת מזומן בכל בורסה' },
      { label: 'ישימות לרועי', value: 'נמוכה מאוד - דורש חשבונות מרובים והון' },
    ],
    verdict: 'הפערים מתועדים כאמיתיים, אבל הלכידה דורשת תשתית והון שאין ב-1,000 דולר. ריאלית: לא ישים.',
    source: { label: 'המאמר (עותק פתוח, LSE)', href: 'https://researchonline.lse.ac.uk/id/eprint/100409/1/Cryptocurrency_Markets_JFE_final_v4.pdf' },
  },
  {
    n: 2,
    name: 'ריוורסל שבועי (קונטרה)',
    what: 'קניית המפסידים של השבוע האחרון ומכירת המנצחים, בנכסים נזילים.',
    facts: [
      { label: 'ראיות', value: 'Int. Review of Financial Analysis 2021; Applied Economics Letters 2020' },
      { label: 'שכבת ראיות', value: 'אקדמי, בעיקר in-sample' },
      { label: 'עלויות', value: 'מחזור שבועי גבוה - עמלות משמעותיות' },
      { label: 'ישימות לרועי', value: 'ישים למבחן נייר על נכסים נזילים' },
    ],
    verdict: 'אפקט מתועד היסטורית, אבל אפקטים כאלה נוטים להיחלש אחרי פרסום. רק מבחן קדימה יגיד. מועמד סביר למעקב נייר.',
    source: { label: 'המאמר המרכזי', href: 'https://www.sciencedirect.com/science/article/pii/S1057521921002349' },
  },
  {
    n: 3,
    name: 'מכירת קולים מכוסים על ביטקוין',
    what: 'החזקת ביטקוין ומכירת אופציות קול מעל המחיר - קצירת פרמיית התנודתיות תמורת ויתור על אפסייד.',
    facts: [
      { label: 'ראיות', value: 'Anchorage Research; Deribit Insights - בקטסטים של ספקים' },
      { label: 'שכבת ראיות', value: 'יישומי/ספק, לא אקדמי' },
      { label: 'עלויות', value: 'עמלות אופציות, ספרד, ניהול פקיעות' },
      { label: 'ישימות לרועי', value: 'נמוכה - גישה לאופציות וגודל מינימלי' },
    ],
    verdict: 'המנגנון אמיתי (פרמיית תנודתיות), אבל הראיות מגיעות מספקים ולא מעבודה מכובדת, והגישה מישראל בגודל קטן בעייתית.',
    source: { label: 'מחקר Anchorage', href: 'https://www.anchorage.com/insights/synthetic-yield-on-bitcoin-implementation-discipline-and-performance-boundaries-of-systematic-covered-call-writing' },
  },
  {
    n: 4,
    name: 'מסחר זוגות (קואינטגרציה)',
    what: 'לונג על נכס אחד ושורט על נכס קשור כשהפער ביניהם חורג מהרגיל.',
    facts: [
      { label: 'ראיות', value: 'Investment Analysts Journal 2023; Emerald SEF' },
      { label: 'שכבת ראיות', value: 'אקדמי, עם שחיקה מתועדת מחוץ למדגם' },
      { label: 'עלויות', value: 'שורט/מינוף, עמלות כפולות, ניטור תדיר' },
      { label: 'ישימות לרועי', value: 'נמוכה - דורש ניהול אקטיבי, לא כמעט-פסיבי' },
    ],
    verdict: 'הקשרים היציבים שהשיטה נשענת עליהם מתפרקים לאורך זמן - מתועד בספרות. לא מתאים לפרופיל שלך.',
    source: { label: 'מחקר השוואתי 2023', href: 'https://www.tandfonline.com/doi/full/10.1080/10293523.2023.2268386' },
  },
  {
    n: 5,
    name: 'פקטור גודל (מטבעות קטנים)',
    what: 'הטיה שיטתית למטבעות קטנים שתשואתם העודפת מתועדת כפקטור.',
    facts: [
      { label: 'ראיות', value: 'Liu, Tsyvinski & Wu, NBER Working Paper 25882' },
      { label: 'שכבת ראיות', value: 'אקדמי, פקטור in-sample' },
      { label: 'עלויות', value: 'נזילות נמוכה, ספרד רחב בזנב' },
      { label: 'ישימות לרועי', value: 'נמוכה - וסותרת את הנתונים שלנו' },
    ],
    verdict: 'מתח ישיר עם הממצאים שלנו: מעקב הנייר על ממקוינס הראה שהזנב הארוך הוא אסון (-70.7% ממוצע מתוקן). לא מומלץ.',
    source: { label: 'NBER w25882 (PDF)', href: 'https://www.nber.org/system/files/working_papers/w25882/w25882.pdf' },
  },
  {
    n: 6,
    name: 'הטיה לתנודתיות נמוכה',
    what: 'בתוך הטופ-50: העדפה שיטתית למטבעות עם תנודתיות נמוכה יחסית.',
    facts: [
      { label: 'ראיות', value: 'Int. Review of Economics & Finance; FRL 2020 (אנומליית low-vol)' },
      { label: 'שכבת ראיות', value: 'אקדמי, in-sample' },
      { label: 'עלויות', value: 'מחזור נמוך יחסית - עמלות מתונות' },
      { label: 'ישימות לרועי', value: 'ישים למבחן נייר פשוט' },
    ],
    verdict: 'מסנן פשוט עם בסיס אקדמי. תוחלת חיובית לא מובטחת, אבל הגיוני למבחן נייר קדימה לצד המומנטום.',
    source: { label: 'מאמר מרכזי', href: 'https://www.sciencedirect.com/science/article/abs/pii/S0275531920301926' },
  },
  {
    n: 7,
    name: 'התאמת גודל פוזיציה לתנודתיות',
    what: 'הקטנת חשיפה כשהתנודתיות קופצת והגדלתה כשהיא נמוכה, על ביטקוין/את׳ריום.',
    facts: [
      { label: 'ראיות', value: 'SSRN 5090097 (קריפטו); Moreira & Muir, J. of Finance 2017 (בסיס כללי)' },
      { label: 'שכבת ראיות', value: 'מאמר עבודה + בסיס אקדמי חזק בשווקים כלליים' },
      { label: 'עלויות', value: 'מחזור נמוך-בינוני' },
      { label: 'ישימות לרועי', value: 'ישים ופשוט למבחן נייר' },
    ],
    verdict: 'זה ניהול סיכון, לא אלפא: משפר יחס תשואה-סיכון בבקטסטים, לא בהכרח תשואה אבסולוטית. הכי "מתנהג כמתועד" מבין העשר.',
    source: { label: 'מאמר הקריפטו', href: 'https://papers.ssrn.com/sol3/papers.cfm?abstract_id=5090097' },
  },
  {
    n: 8,
    name: 'אפקט רישום בבורסה',
    what: 'קנייה סביב רישום של מטבע בבורסה גדולה ומכירה תוך ימים.',
    facts: [
      { label: 'ראיות', value: 'Li, Luo, Wang & Wei, SSRN 4715718' },
      { label: 'שכבת ראיות', value: 'אקדמי, אירועי in-sample' },
      { label: 'עלויות', value: 'דורש מהירות תגובה גבוהה' },
      { label: 'ישימות לרועי', value: 'נמוכה - המחקר שלנו מצא מלכודת front-run' },
    ],
    verdict: 'האפקט מתועד, אבל בדיקה עצמאית קודמת שלנו על רישומים מצאה שהציבור נכנס אחרי שהמחיר כבר זז. לא ישים בפרקטיקה.',
    source: { label: 'מאמר SSRN', href: 'https://papers.ssrn.com/sol3/papers.cfm?abstract_id=4715718' },
  },
  {
    n: 9,
    name: 'קארי בחוזים עתידיים (basis)',
    what: 'לונג ספוט ושורט חוזה עתידי עם פקיעה כשהבסיס השנתי חיובי.',
    facts: [
      { label: 'ראיות', value: '"Crypto Carry", Management Science (מתוך INFORMS)' },
      { label: 'שכבת ראיות', value: 'אקדמי חזק, כתב עת שכבה ראשונה' },
      { label: 'עלויות', value: 'מרג׳ין, מינוף, גדלי חוזה' },
      { label: 'ישימות לרועי', value: 'נמוכה ב-1,000 דולר' },
    ],
    verdict: 'הראיות מהחזקות שיש, אבל זו אותה משפחת קארי כמו דמי מימון (שיטה 2 בחמישיה הקודמת), וההבדל הוא המכשיר בלבד. דורש חשבון חוזים.',
    source: { label: 'המאמר ב-Management Science', href: 'https://pubsonline.informs.org/doi/10.1287/mnsc.2024.05069' },
  },
  {
    n: 10,
    name: 'DCA - ראיות נגד אמונה רווחת',
    what: 'השקעה במנות קבועות (DCA) מול הפקדה חד-פעמית - נבדק כאן כי כולם ממליצים עליו.',
    facts: [
      { label: 'ראיות', value: 'Vanguard Research; סקירות אקדמיות' },
      { label: 'שכבת ראיות', value: 'מחקר ספק מהימן + ספרות' },
      { label: 'עלויות', value: 'אין מיוחדות' },
      { label: 'ישימות לרועי', value: 'ישים, אבל...' },
    ],
    verdict: 'הראיות דווקא נגד: הפקדה חד-פעמית ניצחה DCA בכ-שני שליש מהתקופות במניות. DCA הוא כלי פסיכולוגי נוח, לא יתרון תשואה. נכלל בכוונה כדוגמה הפוכה.',
    source: { label: 'מחקר Vanguard (PDF)', href: 'https://corporate.vanguard.com/content/dam/corp/research/pdf/cost_averaging_invest_now_or_temporarily_hold_your_cash.pdf' },
  },
];

function Overview() {
  return <>
    <Photos label="איור" items={[{ src: hero, alt: 'איור: זכוכית מגדלת מעל גרף נרות ורשימת סימון' }]} />
    <Group label="איך לקרוא את ההערכות" heading>
      <Facts items={[
        { label: 'in-sample', value: 'בקטסט על אותו דאטא שעליו הכלל נבנה - הערכה אופטימית מטבעה' },
        { label: 'out-of-sample', value: 'נבדק על דאטא מאוחר או שונה - חזק יותר, נדיר יותר' },
        { label: 'דאטא אמיתי', value: 'תוצאות שוק בפועל או סיכוי הצלחה קדימה בעולם האמיתי - זה מה שביקשת' },
        { label: 'אזהרת בסיס', value: 'אף מקור כאן לא קובע הסתברות לרווח עתידי; אין אחוזים מומצאים' },
      ]} />
    </Group>
    <Group label="עשר שיטות נוספות, עם מקור מאומת לכל אחת" heading>
      <Text><Paragraph>נבדקו מול הדרישות שלך: עדויות מתועדות מבקטסטים, הערכה כנה לסיכוי על דאטא אמיתי, עלויות, וישימות ב-~1,000 דולר, כמעט-פסיבי, מישראל. שונות מהחמש הקודמות וממעקב המומנטום השבועי.</Paragraph></Text>
    </Group>
    {strategies.map((s) => (
      <Group key={s.n} label={`${s.n}. ${s.name}`} heading>
        <Text><Paragraph>{s.what}</Paragraph></Text>
        <Facts items={s.facts} />
        <Text><Paragraph>{s.verdict}</Paragraph></Text>
        <Text><Paragraph><TextLink href={s.source.href}>{s.source.label}</TextLink></Paragraph></Text>
      </Group>
    ))}
    <Group label="שורה תחתונה" heading>
      <Callout title="מה כן ומה לא" tone="warning">
        אף אחת מהעשר לא מוכחת כ״סבירות גבוהה״ לרווח ב-30 יום הקרובים - וכל מי שמבטיח את זה משקר.
        שלוש ישימות למבחן נייר קדימה תחת תכנון קפוא: ריוורסל שבועי (2), תנודתיות נמוכה (6), והתאמה לתנודתיות (7).
        ארבע לא ישימות בקנה המידה שלך (1, 4, 8, 9). אחת סותרת את הנתונים שלנו (5). אחת ראיות-ספק בלבד (3).
        ואחת היא תזכורת שהאמונה הרווחת לא תמיד נכונה (10).
      </Callout>
    </Group>
    <Closing>נבדק מול מקורות ראשוניים ב-24 באוקטובר 2026. מחקר בלבד - בלי מסחר, בלי חשבונות, בלי כסף.</Closing>
  </>;
}

export function App() {
  return <FileCard>
    <Header title="עשר שיטות קריפטו נוספות במבחן הראיות" fact="24 באוקטובר 2026 · מחקר בלבד" intro="ביקשת עשר שיטות נוספות עם עדויות מבקטסט והערכה כנה לסיכויים על דאטא אמיתי. הנה מה שהראיות באמת אומרות, עם מקור מאומת לכל שיטה והישימות בנסיבות שלך." />
    <Routes><Route path="/" element={<Overview />} /></Routes>
  </FileCard>;
}
