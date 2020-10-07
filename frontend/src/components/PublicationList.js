import React, { Component } from 'react';
import ListItemMixin from 'components/BaseEntities/ListItemMixin';

const formatDate = (date) => {
  const currentDate = new Date(),
    currentDateString = currentDate.toLocaleDateString('ru', {
      year: 'numeric',
      month: 'long',
      day: '2-digit'
    }),
    articlePublishedDate = new Date(date),
    articlePublishedDateString = articlePublishedDate.toLocaleDateString('ru', {
      year: 'numeric',
      month: 'long',
      day: '2-digit'
    }),
    currentYear = currentDate.getFullYear(),
    currentYearIndex = articlePublishedDateString.indexOf(currentYear);

  if (currentDateString === articlePublishedDateString) {
    return 'Сегодня'
  } else if (currentYearIndex >= 0) {
    return articlePublishedDateString.slice(0, currentYearIndex).trim();
  }
  return articlePublishedDate.toLocaleDateString('ru', {
    year: 'numeric',
    month: 'long',
    day: '2-digit'
  })
}

const getDate = (date, isFullDate = false) => {
  const newDate = new Date(date).toLocaleTimeString('ru', {
    year: 'numeric',
    month: 'short',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit'
  }).split(', ');

  if (isFullDate) {
    return {date: newDate[0], time: newDate[1]}
  }

  return {date: formatDate(date), time: newDate[1]};
};

const ReadMore = (props) => {
  const {items, meta} = props,
        isFullDate= meta.data_mart.view_class && meta.data_mart.view_class.indexOf('get_full_date') >= 0 ? true : false;

  return (
    <div className="read-more__container">
      <>
        <div className="panel panel-default read-more">
          <div className="panel-heading">
            <span>Читайте также</span>
          </div>
          <div className="panel-body">
            {items.map((item, index) => {
              const createdAt = getDate(item.extra.created_at, isFullDate);
              return (
                <div className="read-more__item" key={item.id}>
                  <p className="title"><a href={`${item.id}.html`}>{item.entity_name}</a></p>
                  <span className="date_time">
                    {isFullDate ?
                      <>
                        <span className="date">{createdAt.date}</span>
                        <span className="time">&nbsp;—&nbsp;{createdAt.time}</span>
                      </> :
                      <>
                        <span className="time">{createdAt.time}</span>
                        <span className="date">&nbsp;—&nbsp;{createdAt.date}</span>
                      </>}
                  </span>
                  { items.length > 0 && index !== items.length - 1 && <hr/> }
                </div>
              )
            })}
          </div>
        </div>
      </>
    </div>
  );
};

// Container
export default class PublicationList extends Component {

  render() {
    const { items, actions, loading, descriptions, meta } = this.props;
    const datamart = document.querySelector('.read-more');

    let entities_class = "entities list-items";
    entities_class = loading ? entities_class + " ex-state-loading" : entities_class;

    if (datamart) {
      return <ReadMore items={items} meta={meta}/>
    }

    return (
      <div className={entities_class}>
        {items.map(
          (child, i) =>
          <PublicationListItem
              key={i}
              data={child}
              actions={actions}
              loading={loading}
              descriptions={descriptions}
              position={i}
              meta={meta}
          />
        )}
      </div>
    );
  }
}

// Element

class PublicationListItem extends ListItemMixin(Component) {

  getDescriptionText() {
    const { data, descriptions } = this.props,
        descr = descriptions[data.id];

    return descr && descriptions.opened[data.id] ? descr.subtitle || descr.lead : data.extra.short_subtitle;
  }

  static isEqualStr(s1, s2) {
    s1 = s1.replace(/\s+/g, '');
    s2 = s2.replace(/\s+/g, '');

    return s1 === s2;
  }

  getItemBlock(url, data, title, descrText, descriptions){
    const characteristics = data.short_characteristics;
    const createdAt = new Date(data.extra.created_at).toLocaleDateString();

    return (
      <div className="col-md-9">
        <a href={url}>
          <h4>{title}</h4>
          {
            !PublicationListItem.isEqualStr(descrText, data.entity_name) &&
            <p>{descrText}</p>
          }
        </a>
        {descriptions.opened[data.id] && characteristics.length &&
        <div className="ex-description-wrapper">
          <ul className="ex-attrs">
            {characteristics.map((child, i) => (
              <li data-path={child.path} key={i} data-view-class={child.view_class.join(" ")}>
                <strong>{child.name}:&nbsp;</strong>
                {child.values.join(';')}
              </li>
            ))}
          </ul>
        </div>
        }
        <p className="date_time"><i className="fa fa-calendar"/>&nbsp;
          {createdAt}
        </p>
        <span className="padding-left-10 sub-statisitic"><i className="fa fa-eye" aria-hidden="true" />&nbsp;{data.extra.statistic}</span>
      </div>
    )
  }

  render() {
    const { data, meta, descriptions } = this.props,
          url = data.extra && data.extra.url ? data.extra.url : data.entity_url,
          groupSize = data.extra && data.extra.group_size ? data.extra.group_size : 0,
          descrText = this.getDescriptionText();


    let groupDigit = "";
    if (groupSize) {
      groupDigit = (
        <div className="ex-pack">
          <span className="ex-digit">{groupSize}</span>
          <div><div><div></div></div></div>
        </div>
      );
    }

    let characteristics = data.short_characteristics || [],
        marks = data.short_marks || [];

    // let related_data_marts = [];
    if (descriptions[data.id]) {
      characteristics = descriptions[data.id].characteristics || [];
      marks = descriptions[data.id].marks || [];
      // related_data_marts = descriptions[data.id].marks || [];
    }

    const className = "ex-catalog-item list-item" + (groupSize ? " ex-catalog-item-variants" : "") +
        (descriptions.opened[data.id] ? " ex-state-description" : "");

    const title = groupSize && !meta.alike ? data.extra.group_name : data.entity_name,
          itemBlock = this.getItemBlock(url, data, title, descrText, descriptions),
          itemContent = this.getItemContent(url, data, itemBlock, marks);

    return (
      <div className={className}
         onMouseOver={e => this.handleMouseOver(e)}
         onMouseOut={e => this.handleMouseOut(e)}
         style={{minHeight: this.state.minHeight}}>
        {groupDigit}
        {itemContent}
      </div>
    );
  }
}
