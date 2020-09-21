import React, {Component} from 'react';
import {withYMaps, YMaps} from 'react-yandex-maps';
import {YMapInner} from 'components/BaseEntities/YMap';


class PublicationYMap extends YMapInner {
  static getMapConfig(){
     return Object.assign(YMapInner.getMapConfig(), {
        behaviors: [
          'drag',
          'dblClickZoom',
          'rightMouseButtonMagnifier',
          'multiTouch',
        ]
    });
  }

  assembleInfo(item, meta, description) {
    const { marks, characteristics, media, header } = this.assembleInfoVars(item, meta, description);
    let exRibbons = this.exRibbons(marks),
        exTags = this.exTags(marks),
        messageId = description ? description.id : null;

    let annotations = {};
    if (item.extra) {
      for (const [key, val] of Object.entries(item.extra)) {
        if (val instanceof Object && 'name' in val && 'value' in val)
          annotations[key] = val;
      }
    }

    return (
      <div className="ex-map-info"
           onClick={e => {this.handleInfoMouseClick(e, item);}}
           style={item.extra.group_size && {cursor: 'pointer'}}>
        <div className="ex-map-img" dangerouslySetInnerHTML={{__html: marked(media, {sanitize: false})}} />
        {exRibbons}
        <div className="ex-map-descr">
          <h5>{header}</h5>
          <ul className="ex-attrs">
            {characteristics.map(
              (child, i) =>
                <li data-path={child.path} key={i}
                    data-view-class={child.view_class.join(" ")}>
                  <strong>{child.name}:</strong>&nbsp;
                  {child.values.join("; ")}
                </li>
            )}
            {Object.keys(annotations).length !== 0 &&
              <li className="annotation">
                {Object.keys(annotations).map(
                  (key, i) =>
                    <div key={i}>
                      <strong>{annotations[key].name}:&nbsp;</strong>
                      {annotations[key].value instanceof Array ?
                        annotations[key].value.map((val, key) => <span key={key}>{val};&nbsp;</span>)
                      :
                        <span key={key}>{annotations[key].value}</span>
                      }
                    </div>
                )}
              </li>
            }
          </ul>
          {exTags}
        </div>
      </div>
    );
  }

}


const YMapWrapped = withYMaps(PublicationYMap, true, ['templateLayoutFactory']);

const YMap = props => {
  return(
    <YMaps>
      <YMapWrapped {...props} getMapConfig={PublicationYMap.getMapConfig} />
    </YMaps>
  )
};
export default YMap;
