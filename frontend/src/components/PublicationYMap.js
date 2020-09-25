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

    const created_at = new Date(item.extra.created_at);
    const statistic = item.extra.statistic;
    console.log(Object.keys(item.extra).length)

    let annotations = {};
    if (item.extra) {
      for (const [key, val] of Object.entries(item.extra)) {
        if (key === 'created_at') {
          annotations[key] = new Date(val);
        } else if (key === 'statistic') {
          annotations[key] = val;
        }

      }
    }
    console.log(annotations);

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
          </ul>
          {Object.keys(annotations).length &&
            <div className="publication-extra">
              <hr className="publication-extra__hr"/>
              <strong><i className="fa fa-calendar" aria-hidden="true"></i></strong>&nbsp;
              {annotations.created_at.getDate() > 9 ? created_at.getDate() : '0' + created_at.getDate()}.
              {annotations.created_at.getMonth() + 1 > 9 ? created_at.getMonth() + 1 : '0' + (created_at.getMonth() + 1)}.
              {annotations.created_at.getFullYear()}
              <strong className="second"><i className="fa fa-eye" aria-hidden="true"></i></strong>&nbsp;
              {annotations.statistic}
            </div>
          }
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
