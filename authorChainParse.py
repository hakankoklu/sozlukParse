
    author = sys.argv[1]
    #year = sys.argv[2]
    st_time = time.time()
    all_authors = [author]
    parsed_authors = []
    count = 1923
    p_pro = pickle.HIGHEST_PROTOCOL
    ffile = open('author_list_%s' % str(count-1),'r')
    all_authors = pickle.load(ffile)
    ffile.close()
    #screened_authors = all_authors[0:1084]
    ffile = open('screen_list_%s' % str(count),'r')
    screened_authors = pickle.load(ffile)
    ffile.close()
    while len(all_authors) < 55000:
        sc = all_authors[random.randint(0,len(all_authors)-1)]
        while sc in screened_authors:
            sc = all_authors[random.randint(0,len(all_authors)-1)]
        screened_authors.append(sc)
        count = len(screened_authors)
        if count % 10 == 0:
            s_file = open('screen_list_%s' % str(count),'w')
            pickle.dump(screened_authors, s_file, p_pro)
            s_file.close()
        print sc
        try:
            a = get_authors_from_page(sc)
        except urllib2.HTTPError:
            continue
        new_authors = a.keys()
        for aa in new_authors:
            if not aa in all_authors:
                all_authors.append(aa)
        print 'Screened author count: %s' % count
        print 'Current author count: %s' % len(all_authors)
        time_past = time.time()-st_time
        print 'Has been running for: %s seconds' % str(time_past)
        print 'Author/screen: %s' % str(int(len(all_authors)/count))
        print 'Author/time: %s' % str(len(all_authors)/time_past    )
        if count % 10 == 0:
            a_file = open('author_list_%s' % str(count),'w')
            pickle.dump(all_authors, a_file, p_pro)
            a_file.close()
    print all_authors