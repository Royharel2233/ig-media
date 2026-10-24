import React from 'react';
import lot147 from './photos/lot147.png';
import lot342 from './photos/lot342.png';

const css: React.CSSProperties = {};

function Lot({ n, title, img, children }: { n: string; title: string; img: string; children: React.ReactNode }) {
  return (
    <section style={{ marginBottom: 36 }}>
      <h2 style={{ fontSize: 20, margin: '0 0 4px' }}>{title}</h2>
      <div style={{ color: 'var(--ds-ink-2)', fontSize: 14, marginBottom: 12 }}>לוט {n} · מכירה נסגרת ד׳ 11.11.2026, 20:00 (כפי שמוצג באתר)</div>
      <img src={img} alt={title} style={{ width: '100%', borderRadius: 8, display: 'block', marginBottom: 12 }} />
      {children}
    </section>
  );
}

function Line({ k, v }: { k: string; v: React.ReactNode }) {
  return (
    <div style={{ display: 'flex', justifyContent: 'space-between', gap: 12, flexWrap: 'wrap', padding: '8px 0', borderBottom: '1px solid var(--ds-hairline)', fontSize: 15 }}>
      <span style={{ color: 'var(--ds-ink-2)', flexShrink: 0 }}>{k}</span>
      <span style={{ textAlign: 'left' }}>{v}</span>
    </div>
  );
}

export function App() {
  return (
    <main dir="rtl" style={{ maxWidth: 640, margin: '0 auto', padding: '28px 20px 48px', fontFamily: 'system-ui, sans-serif', color: 'var(--ds-ink)' }}>
      <h1 style={{ fontSize: 24, margin: '0 0 6px' }}>קאבום, מכירה 9 — שני לוטים למעקב</h1>
      <p style={{ color: 'var(--ds-ink-2)', fontSize: 15, lineHeight: 1.6, marginTop: 0 }}>
        מתוך הקטלוג בולטים שני לוטים לבדיקה. זו לא המלצת קנייה: המחיר האמיתי נקבע רק בפטיש בשידור החי, וכרגע לא ידוע מחיר שבו העסקה משתלמת בוודאות.
      </p>

      <Lot n="147" title="פוקימון — בוסטר בוקס 30th Celebration סיני, אטום" img={lot147}>
        <Line k="רצפה נוכחית" v={<b>$10 ← $11.53 כולל עמלה ומע״מ</b>} />
        <Line k="מצב ההצעות" v="אין הצעות אמיתיות עדיין — $10 הוא מחיר הפתיחה" />
        <Line k="מכירות שהושלמו (eBay, אותו דגם)" v="‎$72–107 בשבוע האחרון, מרכז ‏~$86–100 (184 מכירות מתועדות)" />
        <Line k="מחיר קמעונאי" v="$106.99" />
        <Line k="אותו בית מכירות, 15.10" v="לוט זהה נמכר בפטיש ב־$240" />
        <p style={{ fontSize: 14, color: 'var(--ds-ink-2)', lineHeight: 1.6 }}>
          הדגם אומת בתמונה: 20 מעטפות × 6 קלפים, גירסה סינית (30周年庆典). במכירה הקודמת הלוט התחיל גם הוא ב־$10 והסתיים ב־$240. אם הלוט יסגר נמוך מספיק, מכירות ה־eBay שהושלמו (‎~$86–100) עשויות להספיק — אבל ערוץ המכירה החוזרת ועלויותיו לא מאומתים.
        </p>
      </Lot>

      <Lot n="342" title="פוקימון — Prismatic Evolutions Binder Collection, אטום לטענת המוכר" img={lot342}>
        <Line k="רצפה נוכחית" v={<b>$20 ← $23.07 כולל עמלה ומע״מ</b>} />
        <Line k="מצב ההצעות" v="הצעה אחת אמיתית מעל מחיר הפתיחה" />
        <Line k="מכירות שהושלמו (PriceCharting)" v="$108.69 — 60 מכירות של אותו מוצר אטום" />
        <Line k="מחיר שוק TCGplayer" v="$105.79 (מחירוני מוכרים, לא מכירות)" />
        <Line k="מצב" v="קרע גלוי בקדמת הקופסה (קרטון/חלון); לא ניתן לוודא שהאיטום המקורי שלם" />
        <p style={{ fontSize: 14, color: 'var(--ds-ink-2)', lineHeight: 1.6 }}>
          המוכר מצהיר ״מארז סגור״ עם קרע קטן מקדימה. בתמונה הקרע נראה משמעותי בחלון הקדמי ובשפת הקרטון. אין השוואת בית-מכירות קודמת לפריט זה.
        </p>
      </Lot>

      <section style={{ background: 'var(--ds-page)', border: '1px solid var(--ds-hairline)', borderRadius: 8, padding: 16, fontSize: 14, lineHeight: 1.7 }}>
        <b>לפני ששווים:</b>
        <ul style={{ margin: '8px 0 0', paddingInlineStart: 20 }}>
          <li>הרצפה אינה המחיר הסופי. במכירה הקודמת: הבוסטר הסיני $180 ← $240, קופסת Hoops $50 ← $100, Origins $45 ← $80.</li>
          <li>עמלת הבית 13% + מע״מ 18% על העמלה בלבד (×1.1534 על הפטיש), לפני משלוח ועמלות אמצעי תשלום; שער הדולר נקבע ביום המכירה.</li>
          <li>תמונות מזהות את המוצר, לא את מצבו או אותנטיותו.</li>
          <li>ערוץ מכירה חוזרת ועלויותיו לא אומתו.</li>
          <li>שעת הסגירה 20:00 כפי שמוצגת באתר (ישראל חזרה לשעון חורף ב־25.10).</li>
          <li>לוטים אחרים בקטלוג: חלקם כבר במחיר שוק מקומי, ובחלקם לא ניתן לאמת את הדגם המדויק מהמודעה — לא נסגרו כאופציות, פשוט לא אומתו.</li>
        </ul>
        <div style={{ marginTop: 12 }}>
          קישורים: <a href="https://il.bidspirit.com/ui/lotPage/kaboom/source/catalog/auction/82443/lot/20197/x?lang=he" style={{ color: 'var(--ds-ink)' }}>לוט 147</a>
          {' · '}
          <a href="https://il.bidspirit.com/ui/lotPage/kaboom/source/catalog/auction/82443/lot/20392/x?lang=he" style={{ color: 'var(--ds-ink)' }}>לוט 342</a>
          {' · '}
          <a href="https://il.bidspirit.com/ui/catalog/auction/kaboom/82443?lang=he" style={{ color: 'var(--ds-ink)' }}>הקטלוג המלא</a>
        </div>
        <div style={{ marginTop: 8, direction: 'ltr', textAlign: 'left', fontSize: 12, color: 'var(--ds-ink-2)' }}>
          Sources: pikaqian.com/sealed/5e51c554-3f2a-43e6-86a1-5a676dfaffeb · pokeunlimited.com/products/pokemon-tcg-simplified-chinese-30th-celebration-booster-box · pricecharting.com/game/pokemon-prismatic-evolutions/binder-collection · pullnomics.com/sealed/prismatic-evolutions-binder-collection · il.bidspirit.com/ui/catalog/auction/kaboom/81261 (תוצאות 15.10)
        </div>
      </section>
    </main>
  );
}
