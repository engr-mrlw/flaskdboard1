export default function FlowRanking({ title, items, labelKey, valueKey }) {
    return (
      <div className="panel flow-ranking">
        <h2>{title}</h2>
  
        <div className="flow-container">
          {items.map((item, index) => (
            <div key={index} className="flow-item">
              <div className="flow-box">
                <div className="flow-label">{item[labelKey]}</div>
                <div className="flow-value">{item[valueKey]}</div>
              </div>
  
              {index < items.length - 1 && (
                <div className="flow-arrow">↓</div>
              )}
            </div>
          ))}
        </div>
      </div>
    );
  }
  