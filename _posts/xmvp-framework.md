---
title: XMVP：一个通过泛型实现的MVP框架2年的演化路
date: 2018-09-21 18:22:15
author: xujiaji
thumbnail: blog/xmvp/banner.png
categories:
 - Android
tags:
    - Android
    - Library
---

> XMVP框架是我的第一个框架，刚从Android起步第一次了解MVP模式时决心写一个自己的东西框架，到现在已运用在我写的多个项目中。虽然两年了，但核心的思路没有改变，到现在变换也不是太多，精简了一些代码，添加了一些功能。

<!-- more -->

## 起步2016
这是个刚出社会找工作痛苦的时期，我个人不太喜欢生活中麻烦的事情。安静是我的本性，于是想写个属于自己的框架，为未来做些铺垫。于是，便有了XMVP，名字“X”是臭不要脸的加上了自己名字的开头字母。

#### 目标
**该框架的目标很简单，为了省掉View、Model、Presenter层之间的依赖实现过程，通过简单的配置，框架自动实现依赖关系**

实现的原理：获取配置的泛型类型，通过反射实例化P层和M层。

#### 代码
**1.** 关键能让我开始做这个框架的核心代码如下：
> 传入对象的Class和需要过滤泛型得的匹配的对象，然后遍历`klass`中配置的泛型判断是不是`filterClass`的子类，如果是则找到了配置的泛型类型。

``` java
public static <T> Class<T> getGenericClass(Class<?> klass, Class<?> filterClass) {
    Type type = klass.getGenericSuperclass(); // 获取父类Class类型，它包含了所配置的泛型类型
    if (type == null || !(type instanceof ParameterizedType)) return null; // 判断是否是泛型类型
    ParameterizedType parameterizedType = (ParameterizedType) type;
    Type[] types = parameterizedType.getActualTypeArguments(); // 由于一个类可能不止配置了一个泛型，获取该对象所有泛型类型
    for (Type t : types) {
        Class<T> tClass = (Class<T>) t;
        if (filterClass.isAssignableFrom(tClass)) { // 通过filterClass找到需要的目标类型
            return tClass;
        }
    }

    return null;
}
```
**2.** 使用也非常简单，精简代码如下所示，4步配置就实现了MVP
 - 首先定义契约（Contract），定义View、Model、Presenter的接口，并且都需要继承自`XContract`
 - 创建Model实现类
 - 创建Presenter实现类继承`XBasePresenter`，泛型中关联View接口和Model实现类
 - 创建View实现类继承`XBaseActivity`或其子类，泛型中关联Presenter实现类

``` java
// 契约
public interface HomeContract {
    interface Presenter extends XContract.Presenter{}
    interface View extends XContract.View{}
    interface Model extends XContract.Model {}
}

// M层实现
public class HomeModel implements HomeContract.Model {}

// P层实现
public class HomePresenter
  extends XBasePresenter<HomeContract.View, HomeModel>
  implements HomeContract.Presenter {}

// V层实现
public class HomeActivity
  extends XBaseActivity<HomePresenter>
  implements HomeContract.View {}
```

**3.** 最初XMVP框架做出时写的一篇文章 [封了一个Android MVP框架，就叫XMVP吧！](https://www.jianshu.com/p/7c71c0d6c150)

---

> 就这样，第一阶段宣告完毕，然后就是优化和修复一些bug，当然上面的`getGenericClass`这个方法也是后期优化过的结果。

## 想偷懒了就开发了`MVPManager`插件，快速生成`XMVP`代码
![](https://raw.githubusercontent.com/xujiaji/MVPManager/master/display/banner.png)
也就是`XMVP`框架开发出来也就1个月之内的事情吧！这时感觉写契约（Contract），写`XMVP`各个实现类，都是重复的劳动力，每一个新的界面就得去创建这么些文件太过辛苦。结果虽然变得有条理有模块，但是工作量有些重复和增加，有些时候配置泛型忘了还需要看之前是怎么配置的。

当时其实也有创建MVP文件的插件之类的东西，但是不符合`XMVP`的实情，泛型还是得自己动手，于是决心自己写一个`intellij`插件，当然在`AS`中也能使用。

#### 创建MVP代码截图，这是最新的创建代码界面的截图
> 在1.0的基础上，增加了可将同一个模块放一个包中或将MVP分在对应的包中的选项；增加了可以不是XMVP框架的情况下使用

![](https://github.com/xujiaji/MVPManager/raw/master/display/update_2_0_0.png)

#### 这是一张动态图，是一张旧版本的演示图。只需要和上面的截图结合来看一下哦
![](https://github.com/xujiaji/MVPManager/raw/master/display/edit_MVPManager.gif)

#### 最后还有个逆向增加或删除XMVP契约中定义方法的功能
> 会同时更新实现类的方法，本人是写出这个功能，但几乎不用的啦

![](https://github.com/xujiaji/MVPManager/raw/master/display/open_change_MVPManager.gif)

#### 刚刚开发出来MVPManager的时候，我也写了篇文章介绍 [这个AS插件能帮你快速管理MVP](https://www.jianshu.com/p/5d528019a76b)

---

> 就这样，第二阶段结束了。其主要目的就是为了解决MVP重复逻辑的代码量问题



## 实践中的更新
在不断的实践运用中也发现了很多没有考虑到或者忽略的问题，其中最映像深刻的不过于有次上线应用的时候，混淆居然会导致无法创建Presenter熬夜找了很久。

还有就是忽略了Fragment有app包和v4包两个地方，框架中只写了一个，考虑的都比较片面。

只有在实践中才能真正的考验，一直以来大概就我和少数的小伙伴在使用。虽然用的比较少，但是写出来后就要对它负责嘛！

#### 使用中的一些个人技巧
**1.** 很多时候，Activity和Presenter，更或者Model都有共用的地方，此时我们需要作出提取抽象。于是我们就需要继承`XBaseActivity`、`XBaseFragment`、`XBasePresenter`再做一层抽象，这样如果以后不想用`XMVP`框架有更好的选择也更好替换哈。如下所示：

> BaseActivity.java

``` java
public abstract class BaseActivity<T extends XBasePresenter> extends XBaseActivity<T> {
  @Override
  public void onInitCircle() {
    super.onInitCircle();
    ButterKnife.bind(this);
  }
}
```
> BasePresenter.java

``` java
public class BasePresenter<T extends XContract.View, E extends XContract.Model> extends XBasePresenter<T, E> {
    protected CompositeDisposable mCompositeDisposable;

    @Override
    public void end() {
        super.end();
        if (mCompositeDisposable != null) {
            mCompositeDisposable.clear();
            mCompositeDisposable = null;
        }
    }
}
```
向上面这样，我们通过一个中间层，处理一些我们需要统一调用的或处理的一些东西

**2.** 对于Presenter回调Model处理后返回的数据监听，我们可以定义一个通用监听接口，如下：

``` java
public interface GenericListener<T> {
    void success(T t);
    void error(int code, String err);
}
```

> 并且，我们可以对这个接口进行实现，我们可以统一对错误信息做些提示或处理

``` java
public abstract class GenericListenerImp<T> implements GenericListener<T> {

  public GenericListenerImp(/*可以传入进来base view或base presenter，如果有错误可以调用对应方法统一处理*/) {

  }

  @Override
  public void error(int code, String err) {
    // 对错误做出统一处理
  }
}
```

**3.** 我们最常用的就是刷新加载列表了，几乎所有app中都需要，并且在同一个应用中的加载逻辑都是一样的，于是我们可以将其抽象出来，使用的时候会非常方便。

> 首先定义一个基础刷新契约，每一个有刷新的view的接口都直接从这里继承

``` java
public interface BaseRefreshContract {

    interface Presenter extends XContract.Presenter {
        /**
         * 请求数据
         */
        void requestLoadListData(int page);

        /**
         * 请求更新列表数据
         */
        void requestUpdateListData();
    }

    interface View <X> extends XContract.View {

        /**
         * 更新列表成功
         */
        void updateListSuccess(List<X> datas, boolean isEnd);

        /**
         * 更新失败
         */
        void updateListFail(String err);

        /**
         * 加载数据成功
         */
        void loadListDataSuccess(List<X> datas, int currentPage, boolean isEnd);

        /**
         * 加载数据失败
         * @param err
         */
        void loadListDataFail(String err);

        /**
         * 数据已经被加载完
         */
        void loadListDateOver();

    }

}
```

> 然后抽象View，这里以Activity为例，Fragment一致。我使用了`SwipeRefreshLayout`作为刷新，`BaseRecyclerViewAdapterHelper`处理填充数据和加载数据

``` java
public abstract class BaseRefreshActivity<E ,X extends BaseQuickAdapter<E, BaseViewHolder>, T extends XBasePresenter> extends BaseActivity<T> implements
        BaseRefreshContract.View<E>,
        BaseQuickAdapter.RequestLoadMoreListener,
        SwipeRefreshLayout.OnRefreshListener {

    protected int currentPage;//当前的页面
    protected X mAdapter;
    protected boolean isEnd;
    protected SwipeRefreshLayout swipeLayout;
    protected RecyclerView mRecyclerView;

    @Override
    public void onInitCircle() {
        super.onInitCircle();
        mAdapter = getAdapter();
        mRecyclerView = getRecyclerView();
        swipeLayout = getSwipeLayout();
        swipeLayout.setOnRefreshListener(this);
        mAdapter.setOnLoadMoreListener(this, mRecyclerView);
        mRecyclerView.setAdapter(mAdapter);
    }


    protected abstract X getAdapter();

    protected abstract SwipeRefreshLayout getSwipeLayout();

    protected abstract RecyclerView getRecyclerView();

    /**
     * 更新列表成功
     */
    @Override
    public void updateListSuccess(List<E> datas, boolean isEnd) {
        this.isEnd = isEnd;
        currentPage = 1;
        mAdapter.setNewData(datas);
        swipeLayout.setRefreshing(false);
        if (isEnd) {
            loadListDateOver();
        } else {
            mAdapter.setEnableLoadMore(true);
            mAdapter.loadMoreComplete();
        }
    }

    /**
     * 更新失败
     */
    @Override
    public void updateListFail(String err) {
        swipeLayout.setRefreshing(false);
        mAdapter.setEnableLoadMore(true);
        ToastUtil.getInstance().showLongT(err);
    }

    /**
     * 加载数据成功
     */
    @Override
    public void loadListDataSuccess(List<E> datas, int currentPage, boolean isEnd) {
        this.currentPage = currentPage;
        this.isEnd = isEnd;
        mAdapter.addData(datas);
        swipeLayout.setEnabled(true);
        mAdapter.loadMoreComplete();
    }

    /**
     * 加载数据失败
     *
     * @param err
     */
    @Override
    public void loadListDataFail(String err) {
        swipeLayout.setEnabled(true);
        mAdapter.loadMoreFail();
        ToastUtil.getInstance().showLongT(err);
    }

    /**
     * 数据已经被加载完
     */
    @Override
    public void loadListDateOver() {
        mAdapter.loadMoreEnd();
    }

    @Override
    public void onRefresh() {
        if (!swipeLayout.isRefreshing())
        {
            swipeLayout.setRefreshing(true);
        }
        getPresenter().requestUpdateListData();
        mAdapter.setEnableLoadMore(false);
    }

    @Override
    public void onLoadMoreRequested() {
        if (isEnd) {
            loadListDateOver();
            return;
        }
        swipeLayout.setEnabled(false);
        getPresenter().requestLoadListData(++currentPage);
    }

    protected BaseRefreshContract.Presenter getPresenter() {
        if (presenter instanceof BaseRefreshContract.Presenter) {
            return  (BaseRefreshContract.Presenter) presenter;
        } else {
            throw new RuntimeException("presenter please extends BaseRefreshContract.Presenter");
        }
    }
}
```

> 使用：定义一个列表页面的契约

``` java
public interface ArticleDetailContract {
    interface View extends BaseRefreshContract.View<CircleMsgEntity.CommentBean> {
    }

    interface Presenter extends BaseRefreshContract.Presenter {
    }

    interface Model extends XContract.Model {
      void catArticleDetails(int articleId, int page, CompositeDisposable cd, NetRequestListener<Result<CircleMsgEntity>> listener);
    }
}
```
> 使用：View实现层，由于这是一个公司项目中的类，省略的所有的无关代码
> `CircleMsgEntity.CommentBean` 是一个Adapter(ArticleCommentAdapter)填充的实体类
> `ArticleCommentAdapter` 是一个继承BaseRecyclerViewAdapterHelper框架中的`BaseQuickAdapter`的类，并且该类是这样的：`public class ArticleCommentAdapter extends BaseQuickAdapter<CircleMsgEntity.CommentBean, BaseViewHolder>` 必须保证Activity第一个泛型和Adapter的第一个泛型类型一致

``` java
public class ArticleDetailActivity extends BaseRefreshActivity<CircleMsgEntity.CommentBean, ArticleCommentAdapter, ArticleDetailPresenter> implements ArticleDetailContract.View {
    @BindView(R.id.recycler)
    RecyclerView recycler;
    @BindView(R.id.refresh)
    SwipeRefreshLayout refresh;

    @Override
    public void onInitCircle() {
        super.onInitCircle();
        onRefresh();
    }

    @Override
    public int layoutId() {
        return R.layout.activity_article_detail;
    }

    @Override
    protected ArticleCommentAdapter getAdapter() {
        return new ArticleCommentAdapter(ArticleCommentAdapter.TYPE_NORMAL);
    }

    @Override
    protected SwipeRefreshLayout getSwipeLayout() {
        refresh.setColorSchemeResources(R.color.yellow);
        return refresh;
    }

    @Override
    protected RecyclerView getRecyclerView() {
        recycler.setLayoutManager(new LinearLayoutManager(this));
        return recycler;
    }

}
```

> 使用： Presenter实现层

``` java
public class ArticleDetailPresenter extends BasePresenter<ArticleDetailContract.View,ArticleDetailModel> implements ArticleDetailContract.Presenter {

    @Override
    public void start() {
        super.start();
        mCompositeDisposable = new CompositeDisposable();
    }

    @Override
    public void requestLoadListData(int page) {
        model.catArticleDetails(view.getArticleId(), page, mCompositeDisposable, new NetRequestListener<Result<CircleMsgEntity>>() {
            @Override
            public void success(Result<CircleMsgEntity> circleMsgEntityResult) {
                ResultListBean<List<CircleMsgEntity.CommentBean>> resultListBean = circleMsgEntityResult.getData().getCommentList();
                view.loadListDataSuccess(resultListBean.getList(), resultListBean.getPage(), resultListBean.getPage() >= resultListBean.getPagecount());
            }

            @Override
            public void error(String err) {
                view.loadListDataFail(err);
            }
        });
    }

    @Override
    public void requestUpdateListData() {
        model.catArticleDetails(view.getArticleId(), 1, mCompositeDisposable, new NetRequestListener<Result<CircleMsgEntity>>() {
            @Override
            public void success(Result<CircleMsgEntity> circleMsgEntityResult) {
                ResultListBean<List<CircleMsgEntity.CommentBean>> resultListBean = circleMsgEntityResult.getData().getCommentList();
                view.updateListSuccess(resultListBean.getList(), resultListBean.getPage() >= resultListBean.getPagecount());
                view.displayArticleDetail(circleMsgEntityResult.getData());
            }

            @Override
            public void error(String err) {
                view.updateListFail(err);
            }
        });
    }

}
```

> Model层，去请求列表数据

``` java
public class ArticleDetailModel implements ArticleDetailContract.Model {
    @Override
    public void catArticleDetails(int articleId, int page, CompositeDisposable cd, NetRequestListener<Result<CircleMsgEntity>> listener) {
        Observer<Result<CircleMsgEntity>> observer = ModelHelper.getObserver(cd, listener, true); // 对rxjava返回的数据进行统一处理
        Http.getInstance().getArticleDetails(articleId, page, observer);
    }
}
```

这样，我们就可以不断的复用`BaseRefreshActivity`、`ArticleDetailContract`来让刷新加载统一，当然在您实际的使用过程中肯定还需要调整。这里只给我了我自己的一些思路和实现方式。

> 如果我们需要其他的抽象时，只需要注意像刷新一样将泛型继承关系标准上就可以啦。如果Model也可以抽取出来，复用时只需要继承抽象出来的Model。

## 目前
目前XMVP框架已更新到`1.2.2`，废弃了一些以前的方法（当然现在还能用）。添加了更多View层的辅助方法，为了偷个懒，就直接展示新增的方法代码啦！

> 基本周期

``` java
/**
 * author: xujiaji
 * created on: 2018/9/4 10:57
 * description: 定义View相关周期 <br /> Define View related Cycle
 */
public interface XViewCycle {

    /**
     * 在 super {@link android.app.Activity#onCreate(Bundle)}之前被调用              <br />  will be called before super class {@link android.app.Activity#onCreate(Bundle)} called
     */
    void onBeforeCreateCircle();

    /**
     * 在 super {@link android.app.Activity#onCreate(Bundle)}之前被调用，并且有Bundle <br />  will be called before super class {@link android.app.Activity#onCreate(Bundle)} called
     * @param savedInstanceState 该参数不可能为null                                  <br /> this parameter cannot be null
     */
    void onBundleHandle(@NonNull Bundle savedInstanceState);

    /**
     * 获取布局的id                                <br /> get layout id
     * 在 {@link #onBeforeCreateCircle }之后被调用 <br /> will be called after {@link #onBeforeCreateCircle } called
     * @return xml布局id                         <br /> xml layout id
     */
    int layoutId();

    /**
     *  在这里面进行初始化                    <br /> initialize here
     *  在 {@link #layoutId()} 之后被调用   <br /> will be called after {@link #layoutId()} called
     */
    void onInitCircle();

    /**
     * 这里面写监听事件                       <br /> write listens event here
     * 在 {@link #onInitCircle()} 之后被调用 <br /> will be called after {@link #onInitCircle()} called
     */
    void onListenerCircle();

}
```
> Activiy中

``` java
/**
 * author: xujiaji
 * created on: 2018/9/11 15:05
 * description: 定义Activity View相关周期 <br /> Define Activity View related Cycle
 */
public interface XActivityCycle extends XViewCycle {
    /**
     * 处理上个页面传递过来的数据 <br /> Handle the data passed from the previous page
     */
    void onIntentHandle(@NonNull Intent intent);
}
```
> Fragment中

``` java
/**
 * author: xujiaji
 * created on: 2018/9/4 10:57
 * description: 定义Fragment View相关周期 <br /> Define Fragment View related Cycle
 */
public interface XFragViewCycle extends XViewCycle {

    /**
     * 处理{@link Fragment#getArguments()} 的值，如果有才会调用  <br /> Handle the value of {@link Fragment#getArguments()} , if it is there, it will be called
     * @param bundle
     */
    void onArgumentsHandle(@NonNull Bundle bundle);

    void onVisible();

    void onInvisible();

    void onLazyLoad();

    /**
     * 忽略{@link #isFirstLoad() }的值，强制刷新数据，但仍要满足 {@link #isFragmentVisible()} && {@link #isPrepared()} <br />
     * Ignore the value of {@link #isFirstLoad() } to force refresh data, but still satisfy {@link #isFragmentVisible()} && {@link #isPrepared()}
     */
    void setForceLoad(boolean forceLoad);

    boolean isForceLoad();

    boolean isPrepared();

    boolean isFirstLoad();

    boolean isFragmentVisible();

    /**
     * 是否是在ViewPager中，默认为true
     * whether in ViewPager, default is true
     * @return
     */
    boolean isInViewPager();
}
```

可以看到Fragment中定义的方法是比较多的，因为由于懒加载比较常用，新增了懒加载。我们如果需要加载数据，可直接在`onLazyLoad()`方法中进行。

> 需要注意：如果Fragment不是和ViewPager结合，需要将`isInViewPager`返回false，默认返回的true。如果不这样，可能会导致通过FragmentManger提交的Fragment无法调用到`onLazyLoad`方法。

## 最后
通过写这个框架学到了思考很多东西，并且后期也会继续更新，我自己写项目中也在使用。可能有些地方考虑的不充足，谢谢大家也可以提建议。当然这只是MVP的一种实现思路，其他的还是有很多的，这里大家也许都有一定了解哈。

XMVP地址：https://github.com/xujiaji/XMVP

欢迎大家Star、Fork、PR (〃'▽'〃)
