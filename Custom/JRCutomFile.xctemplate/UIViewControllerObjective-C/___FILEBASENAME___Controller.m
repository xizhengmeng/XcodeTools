//
//  ___FILENAME___
//  ___PROJECTNAME___
//
//  Created by ___FULLUSERNAME___ on ___DATE___.
//___COPYRIGHT___
//

#import "___FILEBASENAME___.h"
#import <JRUitls/JRNetErrorSolutionViewController.h>

@interface ___FILEBASENAMEASIDENTIFIER___ ()<UITableViewDelegate, UITableViewDataSource,NetworkErrViewDelegate>
@property (nonatomic, strong) JRNoNetWorkingHeaderView *netErrorView;
@property (nonatomic, strong) UITableView *tableView;
@end

@implementation ___FILEBASENAMEASIDENTIFIER___


-(void) dealloc {
    
    [[NSNotificationCenter defaultCenter] removeObserver:self];
}

-(instancetype) init{
    
    self = [super init];
    if (self) {
        
        [self addNotifacatioin];
    }
    return self;
}

- (void)viewDidLoad {
    [super viewDidLoad];
    [self addNavigationBar:@""];
}

- (void)viewDidAppear:(BOOL)animated {
    
    [super viewDidAppear:animated];
}

- (void)viewDidDisappear:(BOOL)animated {
    
    [super viewDidDisappear:animated];
}


- (void)requestData {
    
}

#pragma mark - datasource
- (NSInteger)numberOfSectionsInTableView:(UITableView *)tableView {
    return 1;
}

- (NSInteger)tableView:(UITableView *)tableView numberOfRowsInSection:(NSInteger)section {
    return 1;
}

- (CGFloat)tableView:(UITableView *)tableView heightForRowAtIndexPath:(NSIndexPath *)indexPath {
    return 0;
}

- (UITableViewCell *)tableView:(UITableView *)tableView cellForRowAtIndexPath:(NSIndexPath *)indexPath {
    return [[UITableViewCell alloc] init];
    
}

#pragma mark -- 下拉刷新
-(void)slimeRefreshStartRefresh:(SRRefreshView *)refreshView{
    [self endHeadRefresh:1.0f];
    [self requestData];
}

- (void)addNotifacatioin {
    // Custom initialization
    //app进入活跃状态
    [[NSNotificationCenter defaultCenter] addObserver:self selector:@selector(appWillEnterForeground) name:UIApplicationWillEnterForegroundNotification object:nil];
    //刷新UI
    [[NSNotificationCenter defaultCenter] addObserver:self selector:@selector(requestData) name:RefreshMainUI object:nil];
    //登录成功通知
    [[NSNotificationCenter defaultCenter] addObserver:self selector:@selector(requestData) name:JRApplicationDidLoginNotification object:nil];
    //登录推出通知
    [[NSNotificationCenter defaultCenter] addObserver:self selector:@selector(requestData) name:JRApplicationDidLogoutNotification object:nil];
    //网络状态变化
    [[NSNotificationCenter defaultCenter] addObserver:self selector:@selector(reachabilityChanged:) name:JRkReachabilityChangedNotification object:nil];
}

-(void)appWillEnterForeground
{
    
}

#pragma mark -- 错误页统一处理
- (void)showNetErrorView:(ENetErrorStatus)type{
    
    if (type == ErrorStatus_Default) {
        _tableView.tableHeaderView = nil;
        return;
    }
    if(!_netErrorView){
        _netErrorView = [JRNoNetWorkingHeaderView jr_noNetWorkingHeader:CGRectMake(0, 0, UIScreen_W, UIScreen_H-NAVIGATION_TOTAL_HEIGHT - TabBar_H)];
    }
    
    NSString *image;
    NSString *text;
    NSString *buttonText;
    _netErrorView.customAction = YES;
    @JDJRWeakify(self);
    if(type == ErrorStatus_ServerError){
        
        image = @"com_network_err";
        text = @"网络不稳定";
        buttonText = @"刷新试试";
        [_netErrorView helpButtonWithHidden:NO];
        _netErrorView.action = ^{
            @JDJRStrongify(self);
            
            [self requestData];
        };
    }else if(type == ErrorStatus_NoNetwork){
        image = @"com_network_none";
        text = @"没有连接到网络";
        buttonText = @"查看解决方案";
        [_netErrorView helpButtonWithHidden:NO];
        _netErrorView.action = ^{
            @JDJRStrongify(self);
            
            ClickEntity * entity = [[ClickEntity alloc]init];
            entity.jumpType = 6;
            entity.jumpNavi = 2010;
            [[JRPodsPublic shareInstance] JRPublicJump:entity];
            return;
        };
        
    }else if(type == ErrorStatus_NoData){
        
        image = @"com_data_none";
        text = @"页面数据异常，稍后再试";
        buttonText = @"";
        [_netErrorView helpButtonWithHidden:YES];
        _netErrorView.action = ^{
            @JDJRStrongify(self);
            
            [self requestData];
        };
    }
    _netErrorView.image = image;
    _netErrorView.stateDescription = text;
    _netErrorView.jumpDescription = buttonText;
    
    if (!self.hasData) {
        _tableView.tableHeaderView = _netErrorView;
    }
    else{
        _tableView.tableHeaderView = nil;
    }
}

#pragma mark -- 网络状体变化通知
- (void)reachabilityChanged:(NSNotification* )note{
    
    if (!_tableView) {
        return;
    }
    JRReachability* curReach  = [note object];
    JRNetworkStatus netStatus = [curReach currentReachabilityStatus];
    switch (netStatus)
    {
        case JRReachableViaWiFi:
        case JRReachableViaWWAN:
        {
            [self requestData];
        }
        default:
            break;
    }
}


- (UITableView *)tableView {
    if (_tableView == nil) {
        _tableView = [[UITableView alloc] initWithFrame:CGRectMake(0, NAVIGATION_TOTAL_HEIGHT, UIScreen_W, CONTAINER_VIEW_HEIGHT) style:UITableViewStylePlain];
        _tableView.backgroundColor = [UIColor clearColor];
        _tableView.separatorStyle = UITableViewCellSeparatorStyleNone;
        _tableView.delegate  = self;
        _tableView.dataSource = self;
        _tableView.showsVerticalScrollIndicator = NO;
        [_tableView registerClass:[ServeChannelMainCell class] forCellReuseIdentifier:CELL];
        [self setHeadRefresh:_tableView isLoading:NO];
        [self setHeadRefreshLoadingShort];
        
        // 40像素footer
        UIView *footView = [[UIView alloc] init];
        footView.backgroundColor = [UIColor clearColor];
        footView.frame = CGRectMake(0, 0, UIScreen_W, 20.0f);
        _tableView.tableFooterView = footView;
    }
    return _tableView;
}
@end
