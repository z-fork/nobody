# -*- coding: utf-8 -*-

# CREATE TABLE `knowledge` (
#   `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
#   `name` varchar(64) NOT NULL,
#   `description` text NOT NULL,
#   `parent_id` int(10) unsigned DEFAULT NULL,
#   `left_id` int(10) unsigned NOT NULL,
#   `right_id` int(10) unsigned NOT NULL,
#   `tree_id` int(10) unsigned NOT NULL,
#   `level` int(10) unsigned NOT NULL,
#   PRIMARY KEY (`id`),
#   KEY `idx_name` (`name`),
#   KEY `idx_parent` (`parent_id`),
#   KEY `idx_left` (`left_id`),
#   KEY `idx_right` (`right_id`),
#   KEY `idx_tree` (`tree_id`),
#   KEY `idx_level` (`level`)
# ) ENGINE=InnoDB AUTO_INCREMENT=118163 DEFAULT CHARSET=utf8;

# {
#     "pk": 1,
#     "model": "english.composition",
#     "fields": {
#         "committer": 3,
#         "update_time": "2014-11-30T21:40:01",
#         "title": "The Way to Success",
#         "auditor2": null,
#         "instruction": "",
#         "creation_time": "2014-11-30T21:40:01",
#         "analysis": "\u9898\u76ee\u6240\u7ed9\u7684\u8c1a\u8bed\u51fa\u81ea\u6797\u80af\uff0c\u7406\u89e3\u8d77\u6765\u96be\u5ea6\u4e0d\u5927\u3002\u9898\u76ee\u8981\u6c42\u4ee5\u8fd9\u6761\u8c1a\u8bed\u4e3a\u57fa\u7840\uff0c\u5199\u4e00\u7bc7\u5173\u4e8e\u6210\u529f\u4e4b\u8def\u7684\u6587\u7ae0\u3002\r\n\u672c\u7bc7\u4f5c\u6587\u53ef\u4ee5\u5206\u4e3a\u4e09\u6bb5\u6765\u8fdb\u884c\uff1a\u7b2c\u4e00\u6bb5\u53ef\u4ee5\u63a2\u8ba8\u6210\u529f\u4e4b\u8def\u7684\u65b9\u6cd5\uff1b\u7b2c\u4e8c\u6bb5\u9610\u8ff0\u5e76\u5206\u6790\u9898\u76ee\u4e2d\u7ed9\u51fa\u7684\u6797\u80af\u5173\u4e8e\u6210\u529f\u7684\u8bf4\u6cd5\uff1b\u7b2c\u4e09\u6bb5\u8003\u751f\u53ef\u4ee5\u8c08\u53ca\u81ea\u5df1\u5bf9\u6210\u529f\u4e4b\u8def\u7684\u770b\u6cd5\uff0c\u540c\u65f6\u53ef\u4ee5\u9002\u5f53\u63d0\u51fa\u4e24\u4e09\u6761\u53ef\u884c\u7684\u505a\u6cd5\u3002\r\n\u7b54\u6848\uff1a\r\n",
#         "auditor1": null,
#         "difficulty": 2,
#         "state": 3000,
#         "question_type": 1019,
#         "answer": "There is no doubt that everyone wants to become successful in our life. However, as regards the way to success, people vary from one another in their opinions. Some people hold the view that a strong will overweighs all other factors while some others maintain that intelligence and opportunities are crucial.\r\n\r\nThere are still others who insist that good preparation plays a vital role in achieving success. Abraham Lincoln, one of the greatest presidents in American history, remarked, \"Give me six hours to chop down a tree, and I will spend the first four sharpening the axe.\" From these words, it may safely be concluded that he laid emphasis on preparation before setting out. Actually, the Chinese motto, \"A handy tool makes a handy workman,\" echoes with his words. Both attach utmost importance to full preparation.\r\n\r\nAs far as college students are concerned, we should be down-to-earth and prepare ourselves fully for future success in the highly-competitive society. We are supposed to get ourselves ready, not only academically but also mentally. Only in this way can we face the potential tough situations calmly and finally be on the road to our success.\r\n",
#         "stem": "For this part, you are allowed 30 minutes to write a short essay entitled The Way to Success by commenting on Abraham Lincoln's famous remark, \"Give me six hours to chop down a tree, and I will spend, the first four sharpening the axe.\" You should write at least 150 words but no more than 200 words."
#     }
# },

TEXT = '''INSERT INTO `knowledge` VALUES (115907,'词法','词法',NULL,1,2824,2,0);
INSERT INTO `knowledge` VALUES (115908,'构词法','构词法',115907,2556,2691,2,1);
INSERT INTO `knowledge` VALUES (115909,'词的合成','词的合成',115908,2559,2658,2,2);
INSERT INTO `knowledge` VALUES (115910,'词的合成的定义','词的合成的定义',115909,2656,2657,2,3);
INSERT INTO `knowledge` VALUES (115911,'分类','分类',115909,2560,2655,2,3);
'''

from StringIO import StringIO


def main():
    for line in StringIO(TEXT).readlines():
        values = line[line.index('(')+1: line.index(';')-1].split(',')
        d = {
            'pk': int(values[0]) - 115906,
            'model': 'english.knowledge',
            'fields': {
                'name': eval(values[1]).decode('utf-8'),
                'description': eval(values[2]).decode('utf-8'),
                'parent_id': int(values[3]) - 115906 if values[3].isdigit() else values[3].lower(),
                'left_id': int(values[4]),
                'right_id': int(values[5]),
                'tree_id': int(values[6]),
                'level': int(values[7])
            }
        }
        import json
        print json.dumps(d, indent=4)+','


if __name__ == "__main__":
    main()
