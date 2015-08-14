// MyClass.h
@interface MyClass : NSObject
{
    NSString *value;
    NSTextField *textField;
@private
    NSDate *lastModifiedDate;
}
@property (nonatomic, copy) NSString *value;
@property (nonatomic, strong) IBOutlet NSTextField *textField;
@end

// MyClass.m
// Class extension to declare private property
@interface MyClass ()
@property (nonatomic, strong) NSDate *lastModifiedDate;
@end

@implementation MyClass
@synthesize value;
@synthesize textField;
@synthesize lastModifiedDate;
// implementation continues
@end
