#import "afile.h"

NSDictionary *dictionary = @{@"quattuor": @"four", @"quinque": @"five"};

for (NSString *key in dictionary) {
    NSString *value = [dictionary valueForKey:key];
    NSLog(@"English: %@, Latin: %@", key, value);
}
